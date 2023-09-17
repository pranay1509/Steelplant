document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('verification-form');
    const otpInput = document.getElementById('otp');
    const submitButton = document.getElementById('submit-btn');

    otpInput.addEventListener('input', function() {
        let otpValue = otpInput.value.trim();
        otpValue = otpValue.slice(0, 4); // Keep only the first 4 digits
        otpInput.value = otpValue; // Update the value in the input field
        const isOtpValid = /^\d{4}$/.test(otpValue);
        submitButton.disabled = !isOtpValid;
    });
});
