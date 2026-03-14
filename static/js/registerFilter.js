document.addEventListener("DOMContentLoaded", function () {

    const filter = document.getElementById("gameFilter");

    filter.addEventListener("change", function () {

        let selectedGame = this.value.toLowerCase();

        let rows = document.querySelectorAll("#studentsTable tbody tr");

        rows.forEach(row => {

            let game = row.cells[5].innerText.toLowerCase();

            if (selectedGame === "" || game.includes(selectedGame)) {
                row.style.display = "";
            }
            else {
                row.style.display = "none";
            }

        });

    });

});
function clearFilter(){

const filter = document.getElementById("gameFilter")

filter.value = ""

let rows = document.querySelectorAll("#studentsTable tbody tr")

rows.forEach(row=>{
row.style.display=""
})

}