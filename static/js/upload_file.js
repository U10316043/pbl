document.getElementById("uploadBtn").onchange = function () {
    document.getElementById("uploadFile").value = this.value.split('/').pop().split('\\').pop();
};