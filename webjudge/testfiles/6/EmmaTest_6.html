<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <meta http-equiv='X-UA-Compatible' content='IE=edge'>
    <title>PR02 Ajax EStecha</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>

    <!-- Biblioteca Materialize CSS. Materialize es un framework CSS molt semblant a bootstrap pero amb un estil diferent. -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">

    <!-- JS Per a materialize i una biblioteca de icones de materialize, en aquest cas faig servir les icones block i okay. -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

</head>
<body>
    <!-- Styling i CSS -->
    <style>
        body{
            background-color: #aec6cf;
        }        

        .container{
            position: relative;
            margin: auto;
            text-align: center;
            top: 100px;
            width: 830px;
            border: 1px solid black; 
            padding: 30px 0px 10px 70px;
            background-color: white;
        }

        #cercar{
            width: 650px;
        }

        #pelicula{
            border: 1px solid black;
            margin-right: 65px !important;
            margin-bottom: 50px;
            text-align: left;
        }

        #pelicula > p{
            padding-left: 20px;
        }

    </style>
    <!-- End del style, comença el codi JS-->
    <script>
        // Funcio cercarPelicula. Envia una petició al servidor amb el titol de la pelicula i retorna les pelicules trobades.
        function cercarPelicula(){
            // creem un objecte xmlhttprequest
            var xmlhttp = new XMLHttpRequest();
            // Agafem el valor del input del DNI.
            cercar = document.getElementById("cercar").value;
            // Obrim l'arxiu PHP, en el meu cas virtualitzat al port 8000, amb el parametre get "q" que conté una string amb el titol de la pelicula.
            xmlhttp.open("GET","http://localhost:8000/uf4pr2script.php?q="+cercar,true);
            // fem la peticio
            xmlhttp.send();

            // Comprobem el onreadystatechange per evitar executar codi abans de que ens contesti el servidor.
            // readyState 4 significa resposta per part del servidor, i status 200 significa que ens ha respost correctament-
            xmlhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    // Si no conté res, vol dir que la query no ha retornat un resultat, i que la pelicula no es troba a la base de dades. Netejem els divs.
                    if(this.responseText == ""){
                        document.getElementById("peliculas").innerHTML = this.responseText;
                    // Si conté un valor, vol dir que s'ha trobat a la BDD, aixi que el PHP genera el cuadrat i l'inserim directament al innerhtml.
                    } else {
                        document.getElementById("peliculas").innerHTML = this.responseText;
                    }
                }
            };
        }
        

    </script>

    <div class="container">
        <div class="row">
            <form class="col s20">
            <div class="row">
                <div class="input-field col s20">
                <input id="cercar" type="text" class="text" onkeyup="cercarPelicula()">
                <label for="cercar">Cercar una pelicula...</label>
                </div>
            </div>
            </form>
        </div>
        <!-- div contenidor on aniran totes les pelicules trobades -->
        <div id="peliculas">

        </div>
    </div>
</body>
</html>