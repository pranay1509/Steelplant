document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('signup-form');
  const submitButton = document.getElementById('submit-btn');

  form.addEventListener('input', function() {
      const isFormValid = form.checkValidity();
      submitButton.disabled = !isFormValid;
  });
});
