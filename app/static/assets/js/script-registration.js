document.addEventListener("DOMContentLoaded", function () {
  const registrationForm = document.getElementById("registration-form");

  registrationForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const fullName = document.getElementById("register-nama").value;
    const email = document.getElementById("register-email").value;
    const password = document.getElementById("register-password").value;
    const confirmPassword = document.getElementById(
      "register-confirm-password"
    ).value;

    // Form validation
    if (!fullName || !email || !password || !confirmPassword) {
      showErrorToast("All fields are required.");
      return;
    }

    // Password length validation
    if (password.length < 8) {
      showErrorToast("Password must be at least 8 characters long.");
      return;
    }

    // Password combination of letters and numbers validation
    if (!/^(?=.*[a-zA-Z])(?=.*\d).+$/.test(password)) {
      showErrorToast("Password must contain both letters and numbers.");
      return;
    }

    // Password match validation
    if (password !== confirmPassword) {
      showErrorToast("Password and confirm password do not match.");
      return;
    }

    // Form data
    const formData = {
      name: fullName,
      email: email,
      password: password,
    };

    // Send POST request to the server
    fetch("http://127.0.0.1:5000/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.status === 201) {
          showSuccessToast("Registration successful! Please log in.");
          registrationForm.reset();
        } else {
          return response.json();
        }
      })
      .then((data) => {
        if (data && data.error) {
          showErrorToast(data.error);
        }
      })
      .catch((error) => {
        showErrorToast("An error occurred while processing your request.");
      });
  });

  // Function to display error toast
  function showErrorToast(message) {
    const toastBodyError = document.getElementById("toast-body-error");
    toastBodyError.innerText = message;

    const toastError = new bootstrap.Toast(
      document.getElementById("liveToastError")
    );
    toastError.show();
  }

  // Function to display success toast
  function showSuccessToast(message) {
    const toastBodySuccess = document.getElementById("toast-body-success");
    toastBodySuccess.innerText = message;

    const toastSuccess = new bootstrap.Toast(
      document.getElementById("liveToastSuccess")
    );
    toastSuccess.show();
  }
});
