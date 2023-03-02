function loadingHandler() {
  // let handwritten_file = document.querySelector("#handwritten_file");
  // let software_file = document.querySelector("#software_file");
  // if (handwritten_file.files.length == 0 || software_file.files.length == 0) {
  //   alert("Bitte wählen Sie eine Excel-Datei aus!");
  //   window.location.href = "/";}
 
    let exampleForm = document.querySelector("#loading_form");
    downloadBtn = exampleForm.querySelector(".convert-btn");
    downloadBtn.innerText = "Loading...";
    downloadBtn.style.backgroundColor = "#3cb371";
    downloadBtn.style.borderColor = "#ff6347";
  
}
