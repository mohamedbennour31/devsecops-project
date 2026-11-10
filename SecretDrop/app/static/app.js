
document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("upload-form");
    const fileInput = document.getElementById("file-input");
    const dropZone = document.getElementById("drop-zone");
    const chooseButton = document.getElementById("choose-button");
    const uploadButton = document.getElementById("upload-button");
    const selectedFile = document.getElementById("selected-file");
    const uploadStatus = document.getElementById("upload-status");
    const removeFileButton = document.getElementById("remove-file-button");

    // Verify required HTML elements
    if (
        !form ||
        !fileInput ||
        !dropZone ||
        !chooseButton ||
        !uploadButton ||
        !selectedFile ||
        !uploadStatus ||
        !removeFileButton
    ) {
        console.error("SecretDrop: Required HTML elements are missing.");
        return;
    }

    const MAX_SIZE = 10 * 1024 * 1024;

    const allowedExtensions = new Set([
        "pdf", "doc", "docx", "txt", "csv",
        "xls", "xlsx", "ppt", "pptx",
        "png", "jpg", "jpeg", "gif", "webp"
    ]);

    // Remove selected file
    removeFileButton.addEventListener("click", () => {

        fileInput.value = "";
        selectedFile.textContent = "";
        uploadStatus.textContent = "";
        uploadStatus.className = "mt-3";

        uploadButton.disabled = true;
        uploadButton.textContent = "Upload file";

        removeFileButton.classList.add("d-none");
        removeFileButton.disabled = true;

        chooseButton.disabled = false;
    });

    // Format file size
    function formatSize(bytes) {
        return bytes >= 1024 * 1024
            ? (bytes / (1024 * 1024)).toFixed(2) + " MB"
            : (bytes / 1024).toFixed(1) + " KB";
    }

    // Validate selected file
    function selectFile(file) {

        uploadStatus.textContent = "";
        uploadStatus.className = "mt-3";
        selectedFile.textContent = "";

        uploadButton.disabled = true;
        removeFileButton.disabled = true;
        removeFileButton.classList.add("d-none");

        if (!file) {
            fileInput.value = "";
            return;
        }

        const parts = file.name.split(".");
        const extension = parts.length > 1
            ? parts.pop().toLowerCase()
            : "";

        if (!allowedExtensions.has(extension)) {
            uploadStatus.textContent =
                "Unsupported file type. Choose a document or image.";

            uploadStatus.className = "text-danger mt-3";
            fileInput.value = "";
            return;
        }

        if (file.size > MAX_SIZE) {
            uploadStatus.textContent =
                "File is too large. Maximum allowed size is 10 MB.";

            uploadStatus.className = "text-danger mt-3";
            fileInput.value = "";
            return;
        }

        if (file.size === 0) {
            uploadStatus.textContent = "Empty files are not allowed.";
            uploadStatus.className = "text-danger mt-3";
            fileInput.value = "";
            return;
        }

        selectedFile.textContent =
            file.name + " (" + formatSize(file.size) + ")";

        uploadButton.disabled = false;
        removeFileButton.disabled = false;
        removeFileButton.classList.remove("d-none");
    }

    // Open file selector
    chooseButton.addEventListener("click", () => {
        fileInput.click();
    });

    // File selection
    fileInput.addEventListener("change", () => {
        selectFile(fileInput.files[0]);
    });

    // Drag and drop
    ["dragenter", "dragover"].forEach(eventName => {

        dropZone.addEventListener(eventName, event => {

            event.preventDefault();
            dropZone.classList.add("drag-over");

        });

    });

    ["dragleave", "drop"].forEach(eventName => {

        dropZone.addEventListener(eventName, event => {

            event.preventDefault();
            dropZone.classList.remove("drag-over");

        });

    });

    dropZone.addEventListener("drop", event => {

        const files = event.dataTransfer.files;

        if (files.length > 0) {

            const transfer = new DataTransfer();

            transfer.items.add(files[0]);

            fileInput.files = transfer.files;

            selectFile(files[0]);
        }

    });

    // Upload form submission
    form.addEventListener("submit", event => {

        const file = fileInput.files[0];

        if (!file) {

            event.preventDefault();

            uploadStatus.textContent =
                "Please choose a file first.";

            uploadStatus.className = "text-danger mt-3";

            return;
        }

        uploadButton.disabled = true;
        chooseButton.disabled = true;

        uploadButton.textContent = "Uploading...";

        uploadStatus.textContent = "Uploading your file...";
        uploadStatus.className = "text-primary mt-3";

    });

    // Copy share link
    const copyButton = document.getElementById("copy-link-button");

    if (copyButton) {

        copyButton.addEventListener("click", async () => {

            const input = document.getElementById("share-link");
            const status = document.getElementById("copy-status");

            if (!input || !status) {
                return;
            }

            try {

                await navigator.clipboard.writeText(input.value);

                status.textContent = "Link copied successfully!";
                status.className = "mt-2 mb-0 text-success";

            } catch (error) {

                input.focus();
                input.select();

                status.textContent =
                    "Copy failed. Copy the selected link manually.";

                status.className = "mt-2 mb-0 text-danger";

            }

        });

    }

});
