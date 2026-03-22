
function downloadFilteredPDF() {

    let rows = document.querySelectorAll("#studentsTable tbody tr");
    let selectedGame = document.getElementById("gameFilter").value;
    let data = [];

    rows.forEach(row => {

        if (row.style.display !== "none") {

            data.push({
                name: row.cells[0].innerText,
                branch: row.cells[1].innerText,
                semester: row.cells[2].innerText,
                email: row.cells[3].innerText,
                phone: row.cells[4].innerText,
                game: row.cells[5].innerText
            })

        }

    })

    fetch("/download-filtered-pdf", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            rows: data,
            game: selectedGame
        })
    })
        .then(res => res.blob())
        .then(blob => {

            let url = window.URL.createObjectURL(blob)
            let a = document.createElement("a")
            a.href = url
            a.download = `${selectedGame}_participants.pdf`
            a.click()

        })

}
