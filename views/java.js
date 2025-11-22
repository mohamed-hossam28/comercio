function toggleCartWindow() {
    const cartWindow = document.getElementById('cartWindow');
    cartWindow.style.display = cartWindow.style.display === 'none' ? 'block' : 'none';
    
}

function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    cartItems.forEach(item => {
        const price = parseFloat(item.dataset.price);
        const quantity = parseInt(item.dataset.quantity);
        total += price * quantity;
    });
    document.getElementById('cartTotal').textContent = `$${total.toFixed(2)}`;
}

function display(){
    const cartWindow = document.getElementById('cartWindow');
    cartWindow.style.display ==='none';
}

document.getElementById('cart').addEventListener('click', toggleCartWindow);
document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', (e) => {
        const item = e.target.dataset.item;
        const price = parseFloat(e.target.dataset.price);
        const quantityInput = e.target.parentElement.querySelector('.quantity-input');
        const quantity = parseInt(quantityInput.value);
        const cartItems = document.getElementById('cartItems');
        const existingItem = Array.from(cartItems.children).find(child => child.dataset.item === item);

        if (existingItem) {
            const existingQuantity = parseInt(existingItem.dataset.quantity);
            existingItem.dataset.quantity = existingQuantity + quantity;
            existingItem.querySelector('.item-quantity').textContent = `Quantity: ${existingItem.dataset.quantity}`;
        } else {
            const newItem = document.createElement('div');
            newItem.className = 'cart-item';
            newItem.dataset.item = item;
            newItem.dataset.price = price;
            newItem.dataset.quantity = quantity;
            newItem.innerHTML = `
                <span id="item">${item}</span>
                <span>$${price.toFixed(2)}</span>
                <span class="item-quantity">Quantity: ${quantity}</span>
                <span class="remove-item"><button class="rmo"><i class="fa-solid fa-trash"></i></button></span>
            `;
            cartItems.appendChild(newItem);

            newItem.querySelector('.remove-item').addEventListener('click', () => {
                newItem.remove();
                updateCartTotal();
            });
        }

        updateCartTotal();
        display();
    });
});


document.querySelectorAll('.increase-quantity').forEach(button => {
    button.addEventListener('click', () => {
        const quantityInput = button.parentElement.querySelector('.quantity-input');
        quantityInput.value = parseInt(quantityInput.value) + 1;
    });
});


document.querySelectorAll('.decrease-quantity').forEach(button => {
    button.addEventListener('click', () => {
        const quantityInput = button.parentElement.querySelector('.quantity-input');
        if (quantityInput.value > 1) {
            quantityInput.value = parseInt(quantityInput.value) - 1;
        }
    });
});


function submitx(){
    document.getElementById('userIcon').style.display = 'block';
}


function go(){
    window.location.href = 'web.html?modify=true';
}

window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('modify') === 'true') {
        document.getElementById('userIcon').style.display = 'block';
    }
}
