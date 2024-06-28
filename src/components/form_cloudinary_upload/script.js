(function () {
    initCloudinary();

    function initCloudinary() {
        const cloudinaryDataElement = document.querySelector("#cloudinary-upload-info");

        if(cloudinaryDataElement == null) { console.error("#cloudinary-upload-info not found"); return; }

        const cloudinaryUploadInfo = JSON.parse(cloudinaryDataElement.textContent);

        const hiddenInput = document.querySelector("#" + cloudinaryUploadInfo.input_id);
        
        const myWidget = cloudinary.createUploadWidget(
            {
                cloudName: cloudinaryUploadInfo.cloud_name,
                apiKey: cloudinaryUploadInfo.api_key,
                folder: "materiallending-prototype",
                publicIdPrefix: "product",
                sources: ["local"],
                resourceType: "image",
                clientAllowedFormats: "image",
                multiple: false,
                // theme: window.themeState.appliedTheme === "light" ? "default" : "purple",
                prepareUploadParams: async (cb, params) => {
                    params.public_id = hiddenInput.value.split("/").pop();

                    params.signature = await signUpload(params);
                    cb(params);
                },
            },
                (error, result) => {
                if (!error && result && result.event === "success") {
                    document.querySelector("#upload-image").setAttribute("src", result.info.secure_url);

                    hiddenInput.value = result.info.public_id;
                }
            }
        );

        document.querySelector("#upload-image-field").addEventListener("htmx:beforeCleanupElement", () => {
            myWidget.destroy();
        }, {once: true});
          
        document.querySelector("#upload-widget-button").addEventListener(
            "click",
            function () {
            myWidget.open();
            },
            false
        );

        async function signUpload(params_to_sign) {
            return await fetch(cloudinaryUploadInfo.generate_signature_url, {
                method: "POST",
                body: JSON.stringify(params_to_sign),
                cache: "no-cache",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('input[name="csrfmiddlewaretoken"]').value,
                },
            })
            .then(async (response) => {
                if (!response.ok) {
                    console.error(`Could not sign cloudinary image upload! Status: ${response.status}`);
                    return;
                }
                const result = await response.text();
              
                return result;
            });
        }
    }

})();