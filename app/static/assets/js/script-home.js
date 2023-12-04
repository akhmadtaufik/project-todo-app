$(document).ready(function () {
  // Variabel global untuk melacak ID terakhir
  let lastTaskId = 0;

  var fullHeight = function () {
    $(".js-fullheight").css("height", $(window).height());
  };

  fullHeight();

  $(window).resize(function () {
    fullHeight();
  });

  $("#sidebarCollapse").on("click", function () {
    $("#sidebar").toggleClass("active");
  });

  // Gunakan Fetch API untuk memuat data
  fetch("../data/data-task.json")
    .then((response) => response.json())
    .then((responses) => {
      responses.forEach((response) => {
        // Update ID terakhir
        lastTaskId = Math.max(lastTaskId, response.id);

        // Membuat elemen-elemen HTML yang akan menampilkan task
        let article = $("<article>").addClass("border p-2 m-3 drag");
        article.attr("id", response.id);

        // Membuat elemen-elemen HTML
        let badgeDelete = $("<button>")
          .addClass(
            "badge bg-danger link-underline link-underline-opacity-0 mr-3"
          )
          .attr({
            id: "btn-delete-" + response.id,
            onclick: "deleteTask(this.id)",
            "data-bs-toggle": "modal",
            "data-bs-target": "#modalDelete",
          })
          .text("Delete");

        let badgeEdit = $("<button>")
          .addClass(
            "badge bg-info link-underline link-underline-opacity-0 mr-3"
          )
          .attr({
            id: "btn-edit-" + response.id,
            onclick: "editTask(this)",
            "data-bs-toggle": "modal",
            "data-bs-target": "#modalEdit",
          })
          .text("Edit");

        let h4 = $("<h4>").text(response.title);
        let p = $("<p>").text(response.desc);

        // Menambahkan elemen-elemen ke dalam elemen <article>
        article.append(h4, p, badgeDelete, badgeEdit);

        // Menyisipkan elemen <article> ke dalam elemen yang menampung tugas (todoColumn)
        $("#todo").append(article);
      });
    })
    .catch((error) => console.error("Error fetching data:", error));

  // Fungsi Add Task
  const modalAdd = new bootstrap.Modal(document.getElementById("modalAdd"));
  const btnAdd = $("#btn-add");
  const btnAddTask = $("#modalAdd button.btn-primary");
  const titleInput = $("#task-title");
  const descriptionInput = $("#task-description");

  btnAdd.on("click", function () {
    modalAdd.show();
  });

  btnAddTask.on("click", function () {
    const title = titleInput.val().trim();
    const description = descriptionInput.val().trim();

    if (title !== "" && description !== "") {
      // Increment ID terakhir untuk mendapatkan ID baru
      lastTaskId++;
      const newTask = $("<article>")
        .addClass("border p-2 m-3 drag")
        .attr("id", lastTaskId).html(`
            <h4>${title}</h4>
            <p>${description}</p>
            <button class="badge bg-danger link-underline link-underline-opacity-0 mr-3" data-bs-toggle="modal"
                data-bs-target="#modalDelete" onclick="deleteTask(this)" id="btn-delete-${lastTaskId}">Delete</button>
            <button class="badge bg-info link-underline link-underline-opacity-0 mr-3" data-bs-toggle="modal"
                data-bs-target="#modalEdit" onclick="editTask(this)" id="btn-edit-${lastTaskId}">Edit</button>
        `);

      // Tambahkan tugas baru ke kolom "Todo"
      $("#todo").append(newTask);

      // Kosongkan input setelah menambahkan tugas
      titleInput.val("");
      descriptionInput.val("");

      // Tutup modal setelah menambahkan tugas
      modalAdd.hide();
    }
  });
});
