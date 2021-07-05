var logoutBtn = document.querySelector("#logout-btn")

logoutBtn.onclick = function() {
    $.ajax({
        url : 'logout/',
        type : 'POST',
        contentType : 'application/json',
        success : function(content) {
        },
        error : function(xhr, status) {
        }
      })
}