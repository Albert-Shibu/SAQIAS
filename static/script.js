const file = document.getElementById("file");
const preview = document.getElementById("preview");
const empty = document.getElementById("empty");

// IMPORTANT:
// Your HTML has another element with id="detect" in the navigation.
// So we specifically select the Detect button inside the preview card.
const detect = document.querySelector(".preview > button");

const loading = document.getElementById("loading");
const drop = document.getElementById("drop");


// ============================================================
// SELECT / DROP IMAGE
// ============================================================

function useFile(f) {

    if (!f || !f.type.startsWith("image/")) {
        return alert("Please select an image.");
    }

    if (f.size > 5 * 1024 * 1024) {
        return alert("Maximum file size is 5MB.");
    }


    // Show selected image immediately
    const reader = new FileReader();

    reader.onload = e => {

        preview.src = e.target.result;

        preview.style.display = "block";

        empty.style.display = "none";

        detect.disabled = false;

        detect.classList.add("ready");

        detect.querySelector("span").textContent = "Detect";

        loading.style.display = "none";
    };

    reader.readAsDataURL(f);
}


// ============================================================
// FILE PICKER
// ============================================================

file.onchange = () => {

    useFile(file.files[0]);

};


// ============================================================
// DRAG OVER
// ============================================================

["dragover", "dragenter"].forEach(eventName => {

    drop.addEventListener(eventName, e => {

        e.preventDefault();

        drop.style.borderColor = "#9cff32";

    });

});


// ============================================================
// DRAG LEAVE
// ============================================================

drop.addEventListener("dragleave", e => {

    e.preventDefault();

    drop.style.borderColor = "";

});


// ============================================================
// DROP IMAGE
// ============================================================

drop.addEventListener("drop", e => {

    e.preventDefault();

    drop.style.borderColor = "";

    const droppedFile = e.dataTransfer.files[0];

    if (!droppedFile) {
        return;
    }


    // Put dropped file into file input
    const dataTransfer = new DataTransfer();

    dataTransfer.items.add(droppedFile);

    file.files = dataTransfer.files;

    useFile(droppedFile);

});


// ============================================================
// CAMERA BUTTON
// ============================================================

document.getElementById("camera").onclick = () => {

    file.click();

};


// ============================================================
// DETECTION
// ============================================================

detect.onclick = async () => {

    if (!file.files[0]) {
        return;
    }


    // --------------------------------------------------------
    // Prepare request
    // --------------------------------------------------------

    const fd = new FormData();

    fd.append("image", file.files[0]);


    // --------------------------------------------------------
    // Button state
    // --------------------------------------------------------

    detect.disabled = true;

    detect.querySelector("span").textContent = "Analyzing...";

    loading.style.display = "block";


    try {

        // ----------------------------------------------------
        // Send image to Flask
        // ----------------------------------------------------

        const r = await fetch("/detect", {

            method: "POST",

            body: fd

        });


        const data = await r.json();


        // ----------------------------------------------------
        // Error
        // ----------------------------------------------------

        if (!r.ok) {

            throw new Error(
                data.error || "Detection failed"
            );

        }


        // ====================================================
        // SHOW PROCESSED IMAGE
        // ====================================================

        if (data.image) {

            // Timestamp prevents browser cache
            preview.src =
                data.image + "?t=" + Date.now();

            preview.style.display = "block";

            empty.style.display = "none";

        }


        // ====================================================
        // GET RESULTS
        // ====================================================

        const absorption =
            Number(data.absorption || 0);

        const dry =
            Number(
                data.dry !== undefined
                    ? data.dry
                    : 100 - absorption
            );

        const confidence =
            Number(data.confidence || 0);

        const idlyCount =
            Number(data.idli_count || 0);

        const sambarDetected =
            Boolean(data.sambar_detected);


        // ====================================================
        // SAMBAR ABSORPTION
        // ====================================================

        document.getElementById("percent").textContent =
            absorption.toFixed(1) + "%";


        document.getElementById("absorbed").textContent =
            absorption.toFixed(1) + "%";


        // ====================================================
        // DRY IDLY
        // ====================================================

        document.getElementById("dry").textContent =
            dry.toFixed(1) + "%";


        // ====================================================
        // CONFIDENCE
        // ====================================================

        document.getElementById("confidence").textContent =
            confidence.toFixed(1) + "%";


        // ====================================================
        // CONFIDENCE LABEL
        // ====================================================

        let confidenceText = "Medium Confidence";

        if (confidence >= 80) {

            confidenceText = "High Confidence";

        } else if (confidence < 70) {

            confidenceText = "Low Confidence";

        }

        document.getElementById("confidenceLabel").textContent =
            confidenceText;


        // ====================================================
        // MODEL VERSION
        // ====================================================

        document.getElementById("modelVersion").textContent =
            "SAQIAS Preset v1.0";


        // ====================================================
        // ANALYSIS TIME
        // ====================================================

        document.getElementById("analysisTime").textContent =
            "Instant";


        // ====================================================
        // UPDATE RING
        // ====================================================

        document.getElementById("ring").style.background =
            `conic-gradient(
                #45e99a 0 ${absorption}%,
                #29323d ${absorption}% 100%
            )`;


        // ====================================================
        // AI INSIGHT
        // ====================================================

        let insightText = "";


        if (sambarDetected) {

            if (absorption >= 80) {

                insightText =
                    `This idly has absorbed ${absorption.toFixed(1)}% sambar. ` +
                    "It has entered legendary sambar territory. 🥣";

            } else if (absorption >= 60) {

                insightText =
                    `This idly has absorbed ${absorption.toFixed(1)}% sambar. ` +
                    "A respectable level of sambar absorption.";

            } else {

                insightText =
                    `This idly has absorbed ${absorption.toFixed(1)}% sambar. ` +
                    "There is still plenty of room for more sambar.";

            }

        } else {

            insightText =
                "No sambar detected. The idly appears to be living a dry life.";

        }


        document.getElementById("insight").textContent =
            insightText;


        // ====================================================
        // BUTTON
        // ====================================================

        detect.querySelector("span").textContent =
            "Detect again";


        // ====================================================
        // DEBUG
        // ====================================================

        console.log("===== DETECTION RESULT =====");

        console.log("Preset:", data.image_key);

        console.log("Idly count:", idlyCount);

        console.log("Sambar:", sambarDetected);

        console.log("Absorption:", absorption + "%");

        console.log("Dry:", dry + "%");

        console.log("Confidence:", confidence + "%");

        console.log("============================");


    } catch (e) {

        alert(
            e.message || "Detection failed"
        );

        detect.querySelector("span").textContent =
            "Detect";

    }


    // ========================================================
    // FINISH
    // ========================================================

    detect.disabled = false;

    loading.style.display = "none";

};


// ============================================================
// NAVIGATION
// ============================================================

document.querySelectorAll("nav button").forEach(button => {

    button.onclick = () => {

        document
            .querySelectorAll(".page")
            .forEach(page => {

                page.classList.add("hidden");

            });


        const page =
            document.getElementById(
                button.dataset.page
            );


        if (page) {

            page.classList.remove("hidden");

        }


        document
            .querySelectorAll("nav button")
            .forEach(navButton => {

                navButton.classList.remove("active");

            });


        button.classList.add("active");

    };

});


// ============================================================
// THEME
// ============================================================

document.getElementById("theme").onclick = () => {

    alert(
        "Dark mode is the official IdlySambarAI mode. 🌙"
    );

};