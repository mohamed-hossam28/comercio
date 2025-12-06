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
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'; // Dark background

    const box = document.createElement('div');
    box.className = 'custom-alert-box';
    
    // Safety styles for the White Card
    box.style.backgroundColor = 'white';
    box.style.padding = '30px';
    box.style.borderRadius = '15px';
    box.style.textAlign = 'center';
    box.style.boxShadow = '0 4px 15px rgba(0,0,0,0.2)';
    box.style.minWidth = '300px';

    box.innerHTML = `
        <span class="custom-alert-emoji" style="font-size: 3rem; display:block; margin-bottom: 10px;">${emoji}</span>
        <div class="custom-alert-message" style="font-size: 1.1rem; margin-bottom: 20px; color: #333;">${message}</div>
        <button class="custom-alert-btn" style="background: hsl(178, 63%, 51%); border: none; padding: 10px 25px; border-radius: 20px; font-weight: bold; cursor: pointer;">OK</button>
    `;

    overlay.appendChild(box);
    document.body.appendChild(overlay);

    // Show alert with animation
    setTimeout(() => {
        overlay.classList.add('active');
        overlay.style.opacity = '1';
        overlay.style.visibility = 'visible';
    }, 10);

    // Close handler
    const closeBtn = box.querySelector('.custom-alert-btn');
    closeBtn.addEventListener('click', () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.remove(), 300);
    });
}

// ================================
// REGISTRATION FORM SUBMISSION
// ================================
async function submitRegistration(event) {
    console.log("submitRegistration called"); // DEBUG
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        console.log("Sending fetch request..."); // DEBUG
        const response = await fetch("/register-user", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        console.log("Response received:", result); // DEBUG

        if (response.ok && result.success) {
            console.log("Success, showing alert"); // DEBUG
            showAlert(result.message, "success");
            setTimeout(() => {
                window.location.href = "/";
            }, 1500);
        } else {
            console.log("Failure, showing alert"); // DEBUG
            showAlert(result.message || "Registration failed", "error");
        }
    } catch (error) {
        console.error("Registration error:", error);
        showAlert("An error occurred. Please try again.", "error");
    }
}

// ================================
// PAGE LOAD & EVENTS
// ================================
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded"); // DEBUG

    // 1. Attach Form Submit Listener
    const form = document.querySelector("form[action='/register-user']");
    if (form) {
        console.log("Form found, attaching listener"); // DEBUG
        form.addEventListener("submit", submitRegistration);
    } else {
        console.error("Form NOT found!"); // DEBUG
    }

    // 2. Attach Real-Time Email Check Listener
    const emailInput = document.getElementById('reg_email');
    
    if (emailInput) {
        emailInput.addEventListener('blur', async function() {
            const email = this.value;
            const submitBtn = document.querySelector('.su'); 

            if (!email) return; // Don't check if empty

            try {
                // Fetch check from backend
                const response = await fetch(`/check-email?email=${encodeURIComponent(email)}`);
                const data = await response.json();

                if (data.exists) {
                    // --- EMAIL EXISTS: SHOW POPUP & ERROR ---
                    
                    // 1. Trigger the popup
                    showAlert("This email is already registered!", "error");

                    // 2. Visual feedback on input
                    this.style.border = "1px solid #ff6b6b"; 
                    
                    // 3. Disable submit button
                    if(submitBtn) {
                        submitBtn.disabled = true;
                        submitBtn.style.opacity = "0.5";
                        submitBtn.style.cursor = "not-allowed";
                    }

                } else {
                    // --- EMAIL IS GOOD: CLEAR ERROR ---
                    
                    // Reset border style
                    this.style.border = "none"; 
                    
                    // Enable submit button
                    if(submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.style.opacity = "1";
                        submitBtn.style.cursor = "pointer";
                    }
                }
            } catch (error) {
                console.error("Error checking email:", error);
            }
        });
    }
});