
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
    