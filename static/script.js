function activateImageInput(inputId) {
  const imageInput = document.getElementById(inputId);
  imageInput.click();
}
function openCustomModal() {
  const customModal = document.getElementById("custom-modal");
  customModal.classList.remove("hidden");
}

function closeCustomModal() {
  const customModal = document.getElementById("custom-modal");
  customModal.classList.add("hidden");
}

function showLoading() {
  const loadingElement = document.getElementById("loading");
  loadingElement.classList.remove("hidden");
}

function hideLoading() {
  const loadingElement = document.getElementById("loading");
  loadingElement.classList.add("hidden");
}

function handleImageUpload(input) {
  const selectedFile = input.files[0];

  if (selectedFile) {
      showLoading();

      // You can handle the selected file here
      console.log("Selected File:", selectedFile);

      // You may want to display the selected image
      const imgElement = input.previousElementSibling.previousElementSibling; // Assuming the img element is two elements before the input
      imgElement.src = URL.createObjectURL(selectedFile);

      // Submit the form using JavaScript
      const form = input.form;

      fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
      })
      .then(response => response.json())
      .then(data => {
        // Hide loading indicator
        hideLoading();
        // Display the result in a popup
        // check the input id
        if (input.id === "imageInput-plant") {
          // check if the result class contains "healthy"
          if (data.result.class.includes("healthy")) {
            const customModal = document.getElementById("custom-modal");
            customModal.querySelector("#modal-title").innerText = data.result.class;
            openCustomModal();
          }else{

            const customModal = document.getElementById("custom-modal");
            customModal.querySelector("#modal-title").innerText = data.result.class;
            customModal.querySelector("#cure").innerText = data.result.cure;
            openCustomModal();
          }
        }
        else if(input.id === "imageInput-honeyBee"){
          const customModal = document.getElementById("custom-modal");
          customModal.querySelector("#modal-title").innerText = data.result.class;
          customModal.querySelector("#cure").innerText = data.result.probability+" %";
          openCustomModal();
        }
        else if(input.id === "imageInput-Weed"){
          const customModal = document.getElementById("custom-modal");
          customModal.querySelector("#modal-title").innerText = data.result.class;
          customModal.querySelector("#cure").innerText = data.result.probability+" %";
          openCustomModal();
        }
      })
      .catch(
        error => { 
        console.error('Error:', error);
        // Hide loading indicator on error
        hideLoading();
      });
  }
}

// Select the button to close the navbar
const closeButton = document.querySelector(".absolute .bg-white button");

// Select the navbar itself
const navbar = document.querySelector(".absolute");

// Add a click event listener to the close button
closeButton.addEventListener("click", () => {
  if (!navbar.classList.contains("hidden")) {
    navbar.classList.toggle("hidden");
  }
});

// Add an event listener on the document (or a parent container)
document.addEventListener("click", (event) => {
  if (navbar.classList.contains("hidden") && !navbar.contains(event.target)) {
    navbar.classList.remove("hidden");
  }
});