document.getElementById("resume-form").addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("resume", document.getElementById("resume-file").files[0]);
    formData.append("job", document.getElementById("job-description").value);
    const response = await fetch("/analyze", {
        method: "POST",
        body: formData,
    });
    const result = await response.json();
    document.getElementById("result").innerHTML = `Match Score: ${result.score}`;
});