// JavaScript validation and features
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const submitButton = document.querySelector('input[type="submit"]');
  
    // Disable the submit button by default
    submitButton.disabled = true;
  
    // Validate form fields on input
    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
  
    // Form validation function
    function validateForm() {
      const emailValue = emailInput.value.trim();
      const passwordValue = passwordInput.value.trim();
  
      // Enable or disable the submit button based on form field values
      if (emailValue !== '' && passwordValue !== '') {
        submitButton.disabled = false;
      } else {
        submitButton.disabled = true;
      }
  
      // Add custom validation styles to form fields
      if (emailValue === '') {
        emailInput.classList.add('invalid');
      } else {
        emailInput.classList.remove('invalid');
      }
  
      if (passwordValue === '') {
        passwordInput.classList.add('invalid');
      } else {
        passwordInput.classList.remove('invalid');
      }
    }
  
    // Form submission
    form.addEventListener('submit', function(event) {
      event.preventDefault();
  
      // Display a loading message on form submission
      submitButton.value = 'Loading...';
      submitButton.disabled = true;
  
      // Simulate form submission delay for demonstration purposes
      setTimeout(function() {
        // Display success message and reset form
        alert('Login successful!');
        form.reset();
  
        // Reset submit button
        submitButton.value = 'Confirm';
        submitButton.disabled = true;
      }, 1500);
    });
  });
  