$(document).ready(function () {

            $imgSrc = $('#imgProfile').attr('src');
            var eleman = document.getElementById("savingButt");
            function readURL(input) {

                if (input.files && input.files[0]) {
                    var reader = new FileReader();

                    reader.onload = function (e) {
                        $('#imgProfile').attr('src', e.target.result);
                    };

                    reader.readAsDataURL(input.files[0]);
                }
            }
            $('#btnChangePicture').on('click', function () {
                  $('#profilePicture').click();
            });
            $('#profilePicture').on('change', function () {
                readURL(this);
                console.log(this.files);
              var profileImg = $('#profileImg')
              profileImg.files =  this.files ;
              console.log(profileImg.files);

              eleman.removeAttribute("disabled");
            });

        });
