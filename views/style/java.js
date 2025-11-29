// ================================
// TOGGLE CART WINDOW
// ================================
function toggleCartWindow() {
    const cartWindow = document.getElementById('cartWindow');
    if (!cartWindow) return;
    cartWindow.style.display = cartWindow.style.display === 'none' ? 'block' : 'none';
}

document.getElementById('cart')?.addEventListener('click', toggleCartWindow);


// ================================
// UPDATE CART TOTAL
// ================================
function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;

    cartItems.forEach(item => {
        total += parseFloat(item.dataset.price) * parseInt(item.dataset.quantity);
    });

    const totalEl = document.getElementById('cartTotal');
    if (totalEl) totalEl.textContent = `$${total.toFixed(2)}`;
}


// ================================
// SAVE CART TO LOCAL STORAGE
// ================================
function saveCartToLocalStorage() {
    const cartItems = document.querySelectorAll('.cart-item');

    const cart = Array.from(cartItems).map(item => ({
        name: item.dataset.item,
        id: parseInt(item.dataset.id),
        price: parseFloat(item.dataset.price),
        quantity: parseInt(item.dataset.quantity)
    }));

    localStorage.setItem("cart", JSON.stringify(cart));
}


// ================================
// LOAD CART FROM LOCAL STORAGE
// ================================
function loadCartFromStorage() {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];
    const cartItemsContainer = document.getElementById('cartItems');
    if (!cartItemsContainer) return;

    cartItemsContainer.innerHTML = "";

    cart.forEach(item => {
        // Filter out old items that don't have an ID
        if (item.id) {
            addItemToCartUI(item.name, item.price, item.quantity, item.id);
        }
    });

    updateCartTotal();
}


// ================================
// ADD ITEM TO UI
// ================================
function addItemToCartUI(name, price, quantity, id) {
    const cartItems = document.getElementById('cartItems');
    const existingItem = Array.from(cartItems.children).find(child => child.dataset.item === name);

    if (existingItem) {
        const newQty = parseInt(existingItem.dataset.quantity) + quantity;
        existingItem.dataset.quantity = newQty;
        existingItem.querySelector('.item-quantity').textContent = `Quantity: ${newQty}`;
        updateCartTotal();
        saveCartToLocalStorage();
        return;
    }

    const newItem = document.createElement('div');
    newItem.className = 'cart-item';
    newItem.dataset.item = name;
    newItem.dataset.id = id;
    newItem.dataset.price = price;
    newItem.dataset.quantity = quantity;

    newItem.innerHTML = `
        <span>${name}</span>
        <span>$${price.toFixed(2)}</span>
        <span class="item-quantity">Quantity: ${quantity}</span>
        <button class="remove-item"><i class="fa-solid fa-trash"></i></button>
    `;

    cartItems.appendChild(newItem);

    newItem.querySelector('.remove-item').addEventListener('click', () => {
        newItem.remove();
        updateCartTotal();
        saveCartToLocalStorage();
    });
}


// ================================
// ADD TO CART BUTTONS
// ================================
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', (e) => {
        const name = e.target.dataset.item;
        const id = e.target.dataset.id;
        const price = parseFloat(e.target.dataset.price);
        const quantity = parseInt(e.target.parentElement.querySelector('.quantity-input').value);

        addItemToCartUI(name, price, quantity, id);
        updateCartTotal();
        saveCartToLocalStorage();
    });
});


// ================================
// PRODUCT QUANTITY BUTTONS
// ================================
document.querySelectorAll('.increase-quantity').forEach(button => {
    button.addEventListener('click', () => {
        const q = button.parentElement.querySelector('.quantity-input');
        q.value = parseInt(q.value) + 1;
    });
});

document.querySelectorAll('.decrease-quantity').forEach(button => {
    button.addEventListener('click', () => {
        const q = button.parentElement.querySelector('.quantity-input');
        if (q.value > 1) q.value = parseInt(q.value) - 1;
    });
});


// ================================
// CHECKOUT → SEND TO FASTAPI
// ================================
document.getElementById("checkoutBtn")?.addEventListener("click", async () => {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    const payload = {
        user_id: 1,
        items: cart.map(item => ({
            product_name: item.name,
            product_id: item.id,
            price: item.price,
            quantity: item.quantity
        }))
    };

    try {
        const response = await fetch("http://127.0.0.1:8000/order/checkout", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            alert("Checkout completed!");
            document.getElementById('cartItems').innerHTML = "";
            document.getElementById('cartTotal').textContent = "$0.00";
            localStorage.removeItem("cart");
        } else {
            alert("Checkout failed: " + JSON.stringify(result.detail));
        }

    } catch (err) {
        console.error("Checkout error:", err);
        alert("Error connecting to server.");
    }
});


// ================================
// LOGIN FUNCTION 
// ================================
async function submitx() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    if (!email) {
        document.getElementById("emailError").textContent = "Email is required";
        return;
    }

    if (!password) {
        document.getElementById("passwordError").textContent = "Password is required";
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById("userIcon").style.display = "block";
            document.getElementById("userName").innerText = data.user_name;
            const login_form = bootstrap.Modal.getInstance(document.getElementById('login'));
            login_form.hide();
        } else {
            document.getElementById("Error").textContent = data.message;
        }

    } catch (error) {
        document.getElementById("passwordError").textContent = "Server connection error";
    }
}


// ================================
// GO TO MODIFY PAGE
// ================================
function go() {
    window.location.href = 'web.html?modify=true';
}


// ================================
// PAGE LOAD
// ================================
window.addEventListener("load", () => {
    loadCartFromStorage();

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('modify') === 'true') {
        document.getElementById('userIcon').style.display = 'block';
    }
});
