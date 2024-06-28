window.isMobile = function() {
    let check = false;
    (function(a) {
        if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) {
            check = true;
        }
    })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
}

htmx.onLoad((elt) => {
    bulmaInit(elt);
    webSpeechInit(elt);
});

const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

let speechRecognition;
let activeSpeechRecognitionControl;

function supportsSpeechRecognition() {
    return !!SpeechRecognition;
}

function webSpeechInit(loadedElement) {
    if (!supportsSpeechRecognition()) { return; }

    loadedElement.querySelectorAll('.control.has-speech-recognition').forEach((speechControl, i) => {
        const tempDiv = document.createElement("div");
        tempDiv.innerHTML = `
            <span class="icon speech-recognition-icon is-right">
                <iconify-icon icon="ph:microphone" width="1.5em"></iconify-icon>
                <span class="speech-animation-circle"></span>
            </span>
        `;
        const iconContainer = tempDiv.children[0];

        speechControl.classList.add("has-icons-right");
        speechControl.appendChild(iconContainer);

        const id = i + 1;
        const inputField = speechControl.querySelector('input, textarea');
        const animationCircle = iconContainer.querySelector('.speech-animation-circle');

        if(inputField == null || animationCircle == null) { return; }

        iconContainer.addEventListener('click', (event) => {
            event.stopPropagation();

            if (activeSpeechRecognitionControl != null && activeSpeechRecognitionControl !== id) { return; }

            if(speechRecognition == null) {
                speechRecognition = new SpeechRecognition();
                speechRecognition.lang = document.documentElement.lang || 'en';
                addSpeechRecognitionEventHandlers(inputField, animationCircle);

                speechRecognition.start();
                console.log("speech recognition started");

                activeSpeechRecognitionControl = id;
                animationCircle.classList.add('active');
            }
            else {
                speechRecognition.stop();
                console.log("speech recognition stopped");
            }
        });
    });
}

function addSpeechRecognitionIconEventHandlers() {
    event.stopPropagation();

    if (activeSpeechRecognitionControl != null && activeSpeechRecognitionControl !== id) { return; }

    if(speechRecognition == null) {
        speechRecognition = new SpeechRecognition();
        speechRecognition.lang = document.documentElement.lang || 'en';
        addSpeechRecognitionEventHandlers(inputField, animationCircle);

        speechRecognition.start();
        console.log("speech recognition started");

        activeSpeechRecognitionControl = id;
        animationCircle.classList.add('active');
    }
    else {
        speechRecognition.stop();
        console.log("speech recognition stopped");
    }
}

function addSpeechRecognitionEventHandlers(inputField, animationCircle) {
    speechRecognition.onresult = (event) => {
        inputField.value = event.results[0][0].transcript;
    }
    
    speechRecognition.onnomatch = () => {
        console.log("SpeechRecognition: Speech not recognized.");
    }

    speechRecognition.onerror = (event) => {
        switch (event.error) {
            case "audio-capture":
                console.error("SpeechRecognition Error: Audio capture failed.");
                break;
            case "network":
                console.error("SpeechRecognition Error: Required network communication failed.");
                break;
            case "not-allowed":
                console.log("SpeechRecognition Error: Speech input is not allowed.");
                disableSpeechRecognition();
                break;
            case "service-not-allowed":
                console.log("SpeechRecognition Error: SpeechRecognition service is not allowed.");
                disableSpeechRecognition();
                break;
            case "language-not-supported":
                console.error("SpeechRecognition Error: SpeechRecognition language is not supported.");
                disableSpeechRecognition();
                break;
        }
    }

    speechRecognition.onend = () => {
        speechRecognitionCleanup(animationCircle);
    }
}

function speechRecognitionCleanup(animationCircle) {
    speechRecognition = null;
    activeSpeechRecognitionControl = null;
    animationCircle.classList.remove('active');
}

function disableSpeechRecognition() {
    document.querySelectorAll('.control.has-speech-recognition .speech-recognition-icon').forEach((speechRecognitionIconContainer) => {
        const speechRecognitionIcon = speechRecognitionIconContainer.querySelector('iconify-icon');
        speechRecognitionIcon.setAttribute('icon', 'ph:microphone-slash');

        speechRecognitionIconContainer.addEventListener('click', (event) => {
            event.stopImmediatePropagation();
            event.stopPropagation();
        }, true);
    })
}

function bulmaInit(loadedElement) {
    loadedElement.querySelectorAll('.dropdown').forEach((dropdown) => {
        dropdown.addEventListener('click', (event) => {
            event.stopPropagation();
            dropdown.classList.toggle('is-active');
        });
    });

    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(loadedElement.querySelectorAll('.navbar-burger'), 0);

    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
        // Get the target from the "data-target" attribute
        const target = el.dataset.target;
        const $target = document.getElementById(target);

        el.addEventListener('click', () => {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        el.classList.toggle('is-active');
        $target.classList.toggle('is-active');
        });

        $target.addEventListener('htmx:afterRequest', () => {
            closeNavMenu(el, $target);
        });

        document.body.addEventListener('click', (event) => {
            if(event.target.closest(".navbar") == null) {
                closeNavMenu(el, $target);
            }
        });

    });

    function closeNavMenu(navbarBurger, navbarMenu) {
        if(!navbarBurger.classList.contains('is-active')) return;

        navbarBurger.classList.remove('is-active');
        navbarMenu.classList.remove('is-active');
    }

    loadedElement.querySelectorAll('.notification .delete, .message .delete').forEach((deleteButton) => {
        const deleteable = deleteButton.closest('.notification, .message');

        deleteButton.addEventListener('click', () => {
            deleteable.parentNode.removeChild(deleteable);
        });
    });

    // THEMES
    const STORAGE_KEY = "bulma-theme";
    const SYSTEM_THEME = "system";
    const DEFAULT_THEME = "light";

    window.themeState = {
        chosenTheme: SYSTEM_THEME, // light|dark|system
        appliedTheme: DEFAULT_THEME, // light|dark
        OSTheme: null, // light|dark|null
    };

    const state = window.themeState;

    const $themeCycle = document.getElementById("js-cycle");
    const $themeSwitchers = loadedElement.querySelectorAll(".js-themes a");

    const updateThemeUI = () => {
        if (state.appliedTheme === "light") {
            $themeCycle.className = "theme-cycle button is-sun";
        } else {
            $themeCycle.className = "theme-cycle button is-moon";
        }

        $themeSwitchers.forEach((el) => {
            const swatchTheme = el.dataset.scheme;

            if (state.chosenTheme === swatchTheme) {
                el.classList.add("is-active");
            } else {
                el.classList.remove("is-active");
            }
        });
    };

    const setTheme = (theme, save = true) => {
        state.chosenTheme = theme;
        state.appliedTheme = theme;

        if (theme === SYSTEM_THEME) {
            state.appliedTheme = state.OSTheme;
            document.documentElement.removeAttribute("data-theme");
            window.localStorage.removeItem(STORAGE_KEY);
        } else {
            document.documentElement.setAttribute("data-theme", theme);

            if (save) {
                window.localStorage.setItem(STORAGE_KEY, theme);
            }
        }

        updateThemeUI();
    };

    const toggleTheme = () => {
        if (state.appliedTheme === "light") {
            setTheme("dark");
        } else {
            setTheme("light");
        }
    };

    const detectOSTheme = () => {
        if (!window.matchMedia) {
            // matchMedia method not supported
            return DEFAULT_THEME;
        }

        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
            // OS theme setting detected as dark
            return "dark";
        } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
            return "light";
        }

        return DEFAULT_THEME;
    };

    // On load, check if any preference was saved
    const localTheme = window.localStorage.getItem(STORAGE_KEY);
    state.OSTheme = detectOSTheme();

    if (localTheme) {
            setTheme(localTheme, false);
    } else {
            setTheme(SYSTEM_THEME);
    }

    // Event listeners
    $themeSwitchers.forEach((el) => {
        el.addEventListener("click", () => {
            const theme = el.dataset.scheme;
            setTheme(theme);
        });
    });

    window
        .matchMedia("(prefers-color-scheme: dark)")
        .addEventListener("change", (event) => {
            const theme = event.matches ? "dark" : "light";
            state.OSTheme = theme;
            setTheme(theme);
        });
}

//HTMX
function htmxOpenUrlInNewTabWithCtrlOrCmd(element, event) {
    if (event.detail == null || 
        event.detail.verb !== "get" || 
        event.detail.triggeringEvent.type !== "click" || 
        event.detail.elt !== element)
    {
        return;
    }

    if (event.detail.triggeringEvent.ctrlKey || 
        event.detail.triggeringEvent.metaKey) 
    {
        event.preventDefault();
        window.open(event.detail.path);
    }
}