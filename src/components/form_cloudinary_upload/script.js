if (document.readyState !== 'loading') {
    initCode();
} else {
    document.addEventListener('DOMContentLoaded', function () {
        initCode();
    });
}

function initCode() {
    initCloudinary();
}

function initCloudinary() {
    const cloudinaryDataElement = document.querySelector("#cloudinary-upload-info");

    if(cloudinaryDataElement == null) { console.error("#cloudinary-upload-info not found"); return; }

    const cloudinaryUploadInfo = JSON.parse(cloudinaryDataElement.textContent);

    const hiddenInput = document.querySelector("#" + cloudinaryUploadInfo.input_id);

    const themePalette = window.themeState.appliedTheme === "light"
        ? { // light theme
            window: "#FFFFFF",
            windowBorder: "#90A0B3",
            tabIcon: "#0078FF",
            menuIcons: "#5A616A",
            textDark: "#000000",
            textLight: "#FFFFFF",
            link: "#0078FF",
            action: "#FF620C",
            inactiveTabIcon: "#0E2F5A",
            error: "#F44235",
            inProgress: "#0078FF",
            complete: "#20B832",
            sourceBg: "#E4EBF1"
        }
        : { // dark theme
            window: "#181A2F",
            sourceBg: "#202233",
            windowBorder: "#8E9FBF",
            tabIcon: "#FFFFFF",
            inactiveTabIcon: "#8E9FBF",
            menuIcons: "#2AD9FF",
            link: "#08C0FF",
            action: "#336BFF",
            inProgress: "#00BFFF",
            complete: "#33ff00",
            error: "#EA2727",
            textDark: "#000000",
            textLight: "#FFFFFF"
        };
    
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
            styles: {
                palette: themePalette,
            },
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