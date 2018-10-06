<html> 
<head>   
   <meta name="viewport" content="width=device-width, initial-scale=1.0">

   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

   <link href="css/dropzone base.css" type="text/css" rel="stylesheet" />
   <link href="css/dropzone custom.css" type="text/css" rel="stylesheet" />

   <link href="css/app.css" type="text/css" rel="stylesheet" />

   <script src="js/dropzone.js"></script>
   
   <title>GDP corp</title>

   <?php include 'foldersize.php' ?>

   <script>
      var folderSize = <?php echo folderSize('uploads'); ?> / 500e6;
   </script>
</head>
 
<body>
   <?php include 'header.php' ?>

   <section class="container-fluid">
      <div class="row">
         <div class="col-12 text-center">
            <div class="btn-group my-3" role="group" aria-label="Language selection">
               <button type="button" id="it" class="btn btn-primary">Italiano</button>
               <button type="button" id="en" class="btn btn-light">English</button>
            </div>
         </div>
      </div>

      <div class="card tutorial pb-4">
         <img src="img/uslittle.jpg" alt="Us" id="us-photo">
         <div class="card-body" id="intro-it">
            <h5 class="card-title">Salve a tutti!</h5>

            <p class="my-3">Siamo tre studenti del Politecnico di Milano, stiamo raccogliendo immagini allo scopo di
            sviluppare un sistema per il face matching basato sul machine learning, che potrà essere usato in diverse
            applicazioni, ad esempio per lo sblocco di vari dispositivi attraverso il tuo viso.
            Per raggiungere questo obbiettivo abbiamo bisogno del tuo aiuto!</p>

            <p class="my-3">Abbiamo bisogno di qualche immagine del tuo volto (circa 10 immagini) in pose leggermente differenti (come mostrato nella figura sottostante).
            Puoi indossare occhiali, sorridere e/o scattare foto con diversi sfondi e condizioni di illuminazione,
            ma <b><u>ricordati di guardare la fotocamera</u></b> (come se stessi facendo una fototessera) e che i tratti 
            fondamentali del tuo volto (occhi, bocca, naso ...) dovranno essere chiaramente visibili.</p>

            <p class="my-3">Se vuoi, puoi ripetere la compilazione di questa form più volte in modo da aiutarci di più!</p>

            <p class="my-3">Il nome lasciato durante la compilazione verrà citato nel paper finale del progetto.</p>

            <p class="my-3"><b><u>Le tue foto vengono crittografate, perciò nessuno (e nemmeno noi) potrà accedere alle foto
            in un formato intelleggibile.</u></b></p>
         
            <!-- <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> -->

            </br>
            <b class="mt-2">Esempio di pose</b>
         </div>

         <div class="card-body d-none" id="intro-en">
            <h5 class="card-title">Hi everyone!</h5>

            <p class="my-3">We are three students from Politecnico of Milan, we are collecting images with the aim of
            developing a face matching system based on machine learning that can be used for several application,
            for example to unlock different kind of devices using your face.
            To accomplish this goal we need your help!</p>

            <p class="my-3">We need some images of your face (at least 5 images, but 10 would be perfect) in slightly different poses (as shown in figures below).
            You can wear glasses, smile and/or take pictures with different backgrounds and light illumination,
            but <b><u>remember to look at the camera</u></b> (like if you are taking a passport photo) and that your face
            details (eyes, mouth, nose...) must be clearly visibile.</p>

            <p class="my-3">If you want, you can repeat this process multiple times and help us even more!</p>

            <p class="my-3">The name given during the uploading of the photos will be cited in the final paper of the project.</p>
         
            <p class="my-3"><b><u>Your photos will be encrypted, so no one (and neither us) will be able to access them
            in a readable format.</u></b></p>
            <!-- <p class="card-text"><small class="text-muted">Last updated 3 mins ago</small></p> -->

            </br>
            <b class="mt-2">Face poses example</b>
         </div>

         <div class="row">
            <div class="col"></div>
            <div class="col-xs-12 col-md-8 col-lg-4">
               <img src="img/example.jpg" class="photo-example card-img-bottom px-3" alt="Face poses example">
            </div>
            <div class="col"></div>
         </div>
      </div>
         

      <form id="form" action="upload.php" novalidate>
         <div class="form-group">

         <label for="name" class="py-2">Name (or nickname): </label>
         <div class="input-group">
            <input type="text" name="name" class="form-control" required />
            <div class="invalid-feedback">Please choose a username</div>
         </div>

            <div id="dz" class="dropzone">
               <div class="dz-message">Tap here to upload your photos</div>
            </div>

            <div id="error-few-files" class="alert alert-danger d-none" role="alert">Too few files! Upload at least 5 images :)</div>

            <button type="submit" class="btn btn-md btn-outline-primary d-block mx-auto px-4">Send your images</button>
         </div>
      </form>
      
   </section>

   <?php include 'footer.php' ?>

   <script src="js/app.js"></script>
</body>
</html>