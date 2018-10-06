//var dropzone = new Dropzone("#dz", { url: "upload.php"});
Dropzone.autoDiscover = false;

//var myDropzone = new Dropzone("#dz");

var myDropzone = new Dropzone("#dz", {
  url: "upload.php",
  addRemoveLinks: true,
  maxFilesize: 100, // MB
  parallelUploads: 15,
  autoProcessQueue: false,
  uploadMultiple: true,
  acceptedFiles: "image/*",
  maxFiles: 15,

  init: function() {
    var myDropzone = this;
    let form = document.getElementById('form');

    // First change the button to actually tell Dropzone to process the queue.
    document.querySelector("button[type=submit]").addEventListener("click", function(e) {
      // Make sure that the form isn't actually being sent.
      e.preventDefault();
      e.stopPropagation();

      if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
      }
      form.classList.add('was-validated');

      // check if enough files have been picked
      let errorFewFiles = document.getElementById('error-few-files');
      if(myDropzone.files.length < 5) {
        errorFewFiles.classList.remove('d-none');
        return;
      } else {
        errorFewFiles.classList.add('d-none');
      }

      // check if name is valid and not empty
      let name = document.querySelector("input[name=name]").value;
      name = name.trim();
      if(name.length > 0) {
        myDropzone.processQueue();
      }
    });


    this.on("sending", function(file, xhr, formData) {
      let name = document.querySelector("input[name=name]").value;
      name = name.trim();
      formData.append("name", name);
    });

    this.on("success", function(file, response) {
      //console.log(file);
      //console.log(response);
      if(response.success) {
        window.location = "success.php";
      } else {

      }
    });

  }
  
});

var introIt = document.getElementById('intro-it');
var introEn = document.getElementById('intro-en');

var btnIt = document.getElementById('it');
var btnEn = document.getElementById('en');

btnIt.addEventListener('click', function() {
  introIt.classList.remove('d-none');
  introEn.classList.add('d-none');

  btnIt.classList.remove('btn-light');
  btnIt.classList.add('btn-primary');
  btnEn.classList.remove('btn-primary');
  btnEn.classList.add('btn-light');
});

btnEn.addEventListener('click', function() {
  introIt.classList.add('d-none');
  introEn.classList.remove('d-none');

  btnEn.classList.remove('btn-light');
  btnEn.classList.add('btn-primary');
  btnIt.classList.remove('btn-primary');
  btnIt.classList.add('btn-light');
});

// update progress bar
let sizePercentage = Math.round(folderSize * 100);
let progressBar = document.getElementById('size-progress');
progressBar.style.width = sizePercentage + '%';
progressBar.setAttribute('aria-valuenow', sizePercentage + '%');
progressBar.innerText = sizePercentage + '%';