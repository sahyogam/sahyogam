document.addEventListener('DOMContentLoaded', () => {
    const registerAsSelect = document.getElementById('register-as');
    const organizationForm = document.getElementById('organization-register');
    const volunteerForm = document.getElementById('volunteer-register');
    const formWrapper = document.querySelector('.form-wrapper');

    // Function to switch forms with animation
    function switchForm(formToShow) {
        const formToHide = (formToShow === organizationForm) ? volunteerForm : organizationForm;

        formToHide.classList.add('hidden'); // Hide the other form
        formToShow.classList.remove('hidden');

        // Update form wrapper height to avoid layout jump
        formWrapper.style.height = formToShow.offsetHeight + 'px';
    }

    // Initialize the display
    switchForm(organizationForm); // Default to Organization form

    // Add event listener to the select element
    registerAsSelect.addEventListener('change', function() {
        const selectedValue = this.value;

        if (selectedValue === 'organization') {
            switchForm(organizationForm);
        } else if (selectedValue === 'volunteer') {
            switchForm(volunteerForm);
        }
    });

    // Profile Image Upload Preview (Volunteer Form)
    const profileImageUpload = document.getElementById('profile-image-upload');
    const profileImagePreview = document.getElementById('profile-image-preview');

    if (profileImageUpload && profileImagePreview) {
        profileImageUpload.addEventListener('change', function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profileImagePreview.src = e.target.result;
                }
                reader.readAsDataURL(file);
            } else {
                profileImagePreview.src = 'default-avatar.png';
            }
        });
    }

    // Auto-detect Location (Volunteer Form)
    const autoLocationButton = document.querySelector('.location-button');
    const locationInput = document.getElementById('vol-location');

    if(autoLocationButton && locationInput) {
        autoLocationButton.addEventListener('click', function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function (position) {
                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;
                    locationInput.value = `Latitude: ${latitude}, Longitude: ${longitude}`;
                }, function (error) {
                    alert('Unable to retrieve your location');
                });
            } else {
                alert('Geolocation is not supported by your browser');
            }
        });
    }

     // Prevent form submission for demo purposes
    const volunteerFormElement = document.getElementById('volunteer-form');
    const organizationFormElement = document.querySelector('#organization-register form');

   
    
});
