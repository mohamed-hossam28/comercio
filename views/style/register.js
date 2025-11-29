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
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';

    const box = document.createElement('div');
    box.className = 'custom-alert-box';
    // Inline styles for the box
    box.style.background = 'white';
    box.style.padding = '30px';
    box.style.borderRadius = '15px';
    box.style.textAlign = 'center';
    box.style.maxWidth = '400px';
    box.style.width = '90%';
    box.style.boxShadow = '0 10px 30px rgba(0,0,0,0.2)';

    box.innerHTML = `
        <span class="custom-alert-emoji" style="font-size: 4rem; display: block; margin-bottom: 15px;">${emoji}</span>
        <div class="custom-alert-message" style="font-size: 1.2rem; color: #333; margin-bottom: 25px; font-weight: 500;">${message}</div>
        <button class="custom-alert-btn" style="background: hsl(178, 63%, 51%); color: black; border: none; padding: 10px 30px; border-radius: 25px; font-size: 1rem; font-weight: bold; cursor: pointer;">OK</button>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    // Show alert with animation
    setTimeout(() => overlay.style.opacity = '1', 10);

    // Close handler
    const closeBtn = box.querySelector('.custom-alert-btn');
    closeBtn.addEventListener('click', () => {
        overlay.remove();
    });
}

// ================================
// REGISTRATION FORM SUBMISSION
// ================================
async function submitRegistration(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch("/register-user", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (response.ok && result.success) {
            showAlert(result.message, "success");
            setTimeout(() => {
                window.location.href = "/";
            }, 1500);
        } else {
            showAlert(result.message || "Registration failed", "error");
        }
    } catch (error) {
        console.error("Registration error:", error);
        showAlert("An error occurred. Please try again.", "error");
    }
}

// Attach listener if not using inline onsubmit
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form[action='/register-user']");
    if (form) {
        form.addEventListener("submit", submitRegistration);
    }
});
