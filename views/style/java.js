// ================================
// GET PRODUCTS
// ================================
async function loadCategorizedProducts() {
    const container = document.getElementById('products_container');
    if (!container) return;

    try {
        const response = await fetch('http://127.0.0.1:8000/products/grouped');
        if (!response.ok) throw new Error('Failed to fetch products');

        const groupedProducts = await response.json();
        container.innerHTML = ''; // Clear existing content

        for (const [category, products] of Object.entries(groupedProducts)) {
            // Create category section
            const categorySection = document.createElement('section');
            categorySection.className = 'carousel-section';
            categorySection.id = category; // For anchor linking

            // Category Title
            const title = document.createElement('h2');
            title.className = 'category-title';
            title.textContent = category;
            categorySection.appendChild(title);

            // Carousel Container
            const carouselContainer = document.createElement('div');
            carouselContainer.className = 'carousel-container';

            // Only show buttons if more than 3 products
            if (products.length > 3) {
                // Left Button
                const leftBtn = document.createElement('button');
                leftBtn.className = 'scroll-btn left';
                leftBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
                leftBtn.onclick = () => scrollCarousel(carouselContainer, 'left');
                carouselContainer.appendChild(leftBtn);
            }

            // Scrollable Product Container
            const scrollContainer = document.createElement('div');
            scrollContainer.className = 'product-scroll-container';

            products.forEach(product => {
                // Backend has a typo: stock_avilabilty
                const stockCount = product.stock_avilabilty !== undefined ? product.stock_avilabilty : 0;
                const isOutOfStock = stockCount === 0;
                const lowStock = !isOutOfStock && stockCount < 5;

                const stockClass = isOutOfStock ? 'out-of-stock' : (lowStock ? 'low-stock' : '');
                const stockText = isOutOfStock ? 'Sold Out' : `In Stock: ${stockCount}`;

                const card = document.createElement('div');
                card.className = 'product-card';

                card.innerHTML = `
                    ${isOutOfStock ? '<div class="sold-out-overlay">Sold Out</div>' : ''}
                    <img class="product-image" src="${product.image_url}" alt="${product.name}">
                    <div class="product-details">
                        <div class="product-title">${product.name}</div>
                        <div class="product-price">$${product.price.toFixed(2)}</div>
                        <div class="stock-info ${stockClass}">${stockText}</div>
                        
                        ${!isOutOfStock ? `
                        <div class="quantity-control">
                            <span class="quantity-label">Qty:</span>
                            <input type="number" class="qty-input" value="1" min="1" max="${stockCount}" 
                                onchange="validateQuantity(this, ${stockCount})">
                        </div>
                        ` : ''}

                        <button class="add-btn" 
                            ${isOutOfStock ? 'disabled' : ''}
                            onclick="addToCartWithValidation(this, ${product.id}, '${product.name}', ${product.price}, ${stockCount})">
                            ${isOutOfStock ? 'Sold Out' : 'Add to Cart'}
                        </button>
                    </div>
                `;
                scrollContainer.appendChild(card);
            });

            carouselContainer.appendChild(scrollContainer);

            if (products.length > 3) {
                // Right Button
                const rightBtn = document.createElement('button');
                rightBtn.className = 'scroll-btn right';
                rightBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
                rightBtn.onclick = () => scrollCarousel(carouselContainer, 'right');
                carouselContainer.appendChild(rightBtn);
            }

            categorySection.appendChild(carouselContainer);
            container.appendChild(categorySection);
        }

    } catch (error) {
        console.error('Error loading products:', error);
        container.innerHTML = '<div class="alert alert-danger">Failed to load products. Please try again later.</div>';
    }
}

function scrollCarousel(container, direction) {
    const scrollContainer = container.querySelector('.product-scroll-container');
    const card = scrollContainer.querySelector('.product-card');

    if (!card) return;

    // Calculate dynamic scroll amount: card width + gap
    const cardWidth = card.offsetWidth;
    const gap = 20; // Matches CSS gap
    const scrollAmount = cardWidth + gap;

    if (direction === 'left') {
        scrollContainer.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
        scrollContainer.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
}

function validateQuantity(input, maxStock) {
    let value = parseInt(input.value);
    if (isNaN(value) || value < 1) {
        input.value = 1;
        showAlert("Minimum quantity is 1", "warning");
    } else if (value > maxStock) {
        input.value = maxStock;
        showAlert(`Only ${maxStock} items available in stock`, "warning");
    }
}

async function addToCartWithValidation(btn, id, name, price, maxStock) {
    const card = btn.closest('.product-details');
    const qtyInput = card.querySelector('.qty-input');
    const quantity = parseInt(qtyInput.value);

    if (quantity > maxStock) {
        showAlert(`Cannot add ${quantity} items. Only ${maxStock} in stock.`, "error");
        qtyInput.value = maxStock;
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/products/${id}/purchase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ quantity: quantity })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Purchase failed');
        }

        const result = await response.json();
        const newStock = result.new_stock;

        // Update UI
        const stockInfo = card.querySelector('.stock-info');
        if (newStock === 0) {
            stockInfo.textContent = 'Sold Out';
            stockInfo.className = 'stock-info out-of-stock';
            btn.disabled = true;
            btn.textContent = 'Sold Out';
            card.querySelector('.quantity-control').style.display = 'none';

            // Add overlay
            const productCard = card.closest('.product-card');
            if (!productCard.querySelector('.sold-out-overlay')) {
                const overlay = document.createElement('div');
                overlay.className = 'sold-out-overlay';
                overlay.textContent = 'Sold Out';
                productCard.insertBefore(overlay, productCard.firstChild);
            }
        } else {
            stockInfo.textContent = `In Stock: ${newStock}`;
            if (newStock < 5) {
                stockInfo.className = 'stock-info low-stock';
            }
            // Update max attribute for input
            qtyInput.max = newStock;
            // Update onclick handler with new maxStock
            btn.setAttribute('onclick', `addToCartWithValidation(this, ${id}, '${name}', ${price}, ${newStock})`);
        }

        addToCart(id, name, price, quantity);

    } catch (error) {
        console.error('Purchase error:', error);
        showAlert(error.message, "error");
    }
}

// ================================
// CUSTOM ALERT FUNCTION
// ================================
function showAlert(message, type = 'info') {
    // Remove existing alert if any
    const existingAlert = document.querySelector('.custom-alert-overlay');
    if (existingAlert) existingAlert.remove();

    // Determine emoji based on type
    let emoji = 'ℹ️';
    if (type === 'success') emoji = '🎉';
    if (type === 'error') emoji = '❌';
    if (type === 'warning') emoji = '⚠️';
    if (type === 'wave') emoji = '👋';

    // Create alert elements
    const overlay = document.createElement('div');
    overlay.className = 'custom-alert-overlay';
    // Force critical styles inline to ensure visibility
    overlay.style.position = 'fixed';
    overlay.style.zIndex = '9999';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.display = 'flex';
    overlay.style.justifyContent = 'center';
    overlay.style.alignItems = 'center';

    const box = document.createElement('div');
    box.className = 'custom-alert-box';

    box.innerHTML = `
        <span class="custom-alert-emoji">${emoji}</span>
        <div class="custom-alert-message">${message}</div>
        <button class="custom-alert-btn">OK</button>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    // Show alert with animation
    setTimeout(() => overlay.classList.add('active'), 10);

    // Close handler
    const closeBtn = box.querySelector('.custom-alert-btn');
    closeBtn.addEventListener('click', () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    });
}

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
// ADD TO CART WRAPPER
// ================================
function addToCart(id, name, price, quantity) {
    addItemToCartUI(name, price, quantity, id);
    updateCartTotal();
    saveCartToLocalStorage();
    showAlert(`${name} added to cart!`, "success");
}


// ================================
// CHECKOUT → SEND TO FASTAPI
// ================================
// ================================
// SHOW ORDER SUMMARY
// ================================
function showOrderSummary() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        showAlert("Your cart is empty!", "warning");
        return;
    }

    // Check login status first
    fetch("/me").then(response => {
        if (!response.ok) {
            showAlert("Please login to checkout.", "warning");
            const loginModal = new bootstrap.Modal(document.getElementById('login'));
            loginModal.show();
            return;
        }

        // Populate Summary Modal
        const summaryItems = document.getElementById('orderSummaryItems');
        let total = 0;
        let html = '<ul class="list-group">';

        cart.forEach(item => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;
            html += `
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h6 class="my-0">${item.name}</h6>
                        <small class="text-muted">Quantity: ${item.quantity} x $${item.price.toFixed(2)}</small>
                    </div>
                    <span class="text-muted">$${itemTotal.toFixed(2)}</span>
                </li>
            `;
        });

        html += '</ul>';
        summaryItems.innerHTML = html;
        document.getElementById('orderSummaryTotal').textContent = `$${total.toFixed(2)}`;

        // Show Modal
        const summaryModal = new bootstrap.Modal(document.getElementById('orderSummaryModal'));
        summaryModal.show();

        // Close Cart Window
        const cartWindow = document.getElementById('cartWindow');
        if (cartWindow) cartWindow.style.display = 'none';
    });
}

// ================================
// CHECKOUT → SHOW SUMMARY
// ================================
document.getElementById("checkoutBtn")?.addEventListener("click", showOrderSummary);

// ================================
// CONFIRM ORDER → SEND TO FASTAPI
// ================================
document.getElementById("confirmOrderBtn")?.addEventListener("click", async () => {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    // Close summary modal
    const summaryModalEl = document.getElementById('orderSummaryModal');
    const summaryModal = bootstrap.Modal.getInstance(summaryModalEl);

    const payload = {
        user_id: 0,
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
            summaryModal.hide();
            showAlert("Checkout successfully! 🎉", "success");
            document.getElementById('cartItems').innerHTML = "";
            document.getElementById('cartTotal').textContent = "$0.00";
            localStorage.removeItem("cart");
        } else {
            showAlert("Checkout failed: " + (result.message || JSON.stringify(result.detail)), "error");
        }

    } catch (err) {
        console.error("Checkout error:", err);
        showAlert("Error connecting to server.", "error");
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
        document.getElementById("Error").textContent = "Email is required";
        return;
    }

    if (!password) {
        document.getElementById("Error").textContent = "Password is required";
        return;
    }

    try {
        const response = await fetch("/login", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            // Update UI
            updateAuthUI(true, data.user_name);

            // Close modal
            const loginModalEl = document.getElementById('login');
            const loginModal = bootstrap.Modal.getInstance(loginModalEl);
            loginModal.hide();
        } else {
            document.getElementById("Error").textContent = data.message || "Login failed";
        }

    } catch (error) {
        document.getElementById("Error").textContent = "Server connection error";
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
// ================================
// AUTH HELPERS
// ================================
function updateAuthUI(isLoggedIn, userName = "") {
    const loginBtn = document.getElementById("log");
    const logoutBtn = document.getElementById("logoutBtn");
    const userIcon = document.getElementById("userIcon");
    const userNameEl = document.getElementById("userName");

    if (isLoggedIn) {
        if (loginBtn) loginBtn.style.display = "none";
        if (logoutBtn) logoutBtn.style.display = "inline-block";
        if (userIcon) userIcon.style.display = "block";
        if (userNameEl) userNameEl.innerText = userName;
    } else {
        if (loginBtn) loginBtn.style.display = "inline-block";
        if (logoutBtn) logoutBtn.style.display = "none";
        if (userIcon) userIcon.style.display = "none";
        if (userNameEl) userNameEl.innerText = "";
    }
}

async function checkLoginStatus() {
    try {
        const response = await fetch("/me");
        if (response.ok) {
            const data = await response.json();
            updateAuthUI(true, data.user_name);
        } else {
            updateAuthUI(false);
        }
    } catch (error) {
        console.error("Error checking login status:", error);
        updateAuthUI(false);
    }
}

async function logout() {
    try {
        await fetch("/logout", { method: "POST" });
        updateAuthUI(false);
        showAlert("👋 Logged out successfully!<br>See You Soon 😊", "wave");
    } catch (error) {
        console.error("Logout error:", error);
    }
}

document.getElementById("logoutBtn")?.addEventListener("click", (e) => {
    e.preventDefault();
    logout();
});

// ================================
// PROFILE MANAGEMENT
// ================================
async function openProfileModal() {
    try {
        const response = await fetch("/me");
        if (!response.ok) {
            showAlert("Please login to view profile.", "error");
            return;
        }
        const data = await response.json();

        document.getElementById('p_firstName').value = data.first_name || "";
        document.getElementById('p_lastName').value = data.last_name || "";
        document.getElementById('p_phone').value = data.phone || "";
        document.getElementById('p_country').value = data.country || "";
        document.getElementById('p_dob').value = data.dob || "";
        document.getElementById('p_password').value = "";

        const modalElement = document.getElementById('profileModal');
        if (modalElement) {
            const profileModal = new bootstrap.Modal(modalElement);
            profileModal.show();
        }

    } catch (error) {
        console.error("Error fetching profile:", error);
        showAlert("Error loading profile data.", "error");
    }
}

async function saveProfile() {
    const formData = new FormData();
    formData.append("first_name", document.getElementById('p_firstName').value);
    formData.append("last_name", document.getElementById('p_lastName').value);
    formData.append("phone", document.getElementById('p_phone').value);
    formData.append("country", document.getElementById('p_country').value);
    formData.append("dob", document.getElementById('p_dob').value);

    const password = document.getElementById('p_password').value;
    if (password) {
        formData.append("password", password);
    }

    try {
        const response = await fetch("/update-profile", {
            method: "PUT",
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            showAlert("Profile updated successfully! 🎉", "success");
            const profileModalEl = document.getElementById('profileModal');
            const profileModal = bootstrap.Modal.getInstance(profileModalEl);
            profileModal.hide();

            if (result.user_name) {
                document.getElementById("userName").innerText = result.user_name;
            }
        } else {
            showAlert("Update failed: " + (result.message || "Unknown error"), "error");
        }
    } catch (error) {
        console.error("Error updating profile:", error);
        showAlert("Error connecting to server.", "error");
    }
}

const userIcon = document.getElementById("userIcon");
if (userIcon) {
    userIcon.addEventListener("click", (e) => {
        e.preventDefault();
        openProfileModal();
    });
}

// ================================
// PAGE LOAD
// ================================
window.addEventListener("load", () => {
    loadCategorizedProducts();
    loadCartFromStorage();
    checkLoginStatus();
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('modify') === 'true') {
        document.getElementById('userIcon').style.display = 'block';
    }
});


