document.addEventListener("DOMContentLoaded", function () {
  // Function to handle login form submission
  function handleLoginFormSubmit(e) {
    e.preventDefault(); // Prevent the default form behavior

    // Get the email and password values from the form
    const email = document.getElementById("login-email").value;
    const password = document.getElementById("login-password").value;

    // Form validation
    if (!email || !password) {
      // Display error message using Bootstrap Toast
      showToast("Email and password are required.");
      return;
    }

    // Collect login data in JSON object
    const loginData = {
      email: email,
      password: password,
    };

    // Configure POST request to the server
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:5000/api/auth/login", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader(
      "Authorization",
      "Bearer ${localStorage.getItem('refresh_token')}"
    );

    // Respond to changes in request status
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4) {
        // Request completed
        if (xhr.status == 200) {
          // OK response status
          const responseData = JSON.parse(xhr.responseText);

          // Save access token in local storage
          localStorage.setItem("access_token", responseData.access_token);

          // Redirect user to the main page
          window.location.href = "http://127.0.0.1:5000";
        } else {
          // Display error message from server response using Bootstrap Toast
          showToast("Error: " + xhr.statusText);
        }
      }
    };

    // Send POST request to the server with login data
    xhr.send(JSON.stringify(loginData));
  }

  // Function to display Bootstrap Toast
  function showToast(message) {
    const toastBody = document.getElementById("toast-body");
    toastBody.innerHTML = message;

    const toast = new bootstrap.Toast(document.getElementById("liveToast"));
    toast.show();
  }

  // Set the handleLoginFormSubmit function to handle login form submission
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", handleLoginFormSubmit);
  } else {
    console.error("Element with ID 'login-form' not found");
  }
});
