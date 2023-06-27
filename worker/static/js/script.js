const imageInput = document.getElementById('imageInput');
const videoInput = document.getElementById('videoInput');
const cameraInput = document.getElementById('cameraInput');
const imageBtn = document.getElementById('imageBtn');
const videoBtn = document.getElementById('videoBtn');
const cameraBtn = document.getElementById('cameraBtn');
const submitBtn = document.getElementById('submitBtn');


imageBtn.addEventListener('click', () => {
    imageInput.click();
    imageInput.addEventListener('change', () => {
        const preview = document.getElementById('previewImg');
        const file = imageInput.files[0];
        const reader = new FileReader();
        if (file) {
            reader.readAsDataURL(file);
            preview.removeAttribute('hidden');
            submitBtn.style.visibility = 'visible';
        } else {
            preview.src = "";
        }
        reader.onloadend = function () {
            preview.src = reader.result;
        }


    });
});

videoBtn.addEventListener('click', () => {
    videoInput.click();
    videoInput.addEventListener('change', () => {
        const preview = document.getElementById('previewVideo');
        const file = videoInput.files[0];
        const reader = new FileReader();
        if (file) {
            reader.readAsDataURL(file);
            preview.removeAttribute('hidden');
            submitBtn.style.visibility = 'visible';
        } else {
            preview.src = "";
        }
        reader.onloadend = function () {
            preview.src = reader.result;
        }


    });
});

cameraBtn.addEventListener('click', () => {
    const preview = document.getElementById('previewVideo');
    let { mediaDevices } = navigator;
    preview.muted = true;

    // Accessing the user camera and video.
    mediaDevices
        .getUserMedia({
            video: true,
            audio: true,
        })
        .then((stream) => {

            // Changing the source of video to current stream.
            preview.srcObject = stream;

                preview.removeAttribute('hidden');
                preview.play();

        })
        .catch(alert);
});