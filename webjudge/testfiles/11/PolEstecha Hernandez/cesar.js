class Cesar {
  diccionari = "ABCÇDEFGHIJKLMNÑOPQRSTUVWYXZ0123456789";
  entrada = ""
  clau = 0;
  sortida = "";
  // Constructor de la clase
  constructor(entrada, clau) {
    this.entrada = entrada;
    this.clau = clau;
  }

  xifrar() {
    var nuevafrase = ""; // Guardar nueva frase 
    var dictsplit = this.diccionari.split(""); // Separar el diccionario en un array
    this.entrada = this.entrada.toUpperCase(); // Todo a mayusculas
    // Por cada letra:
    // -> Buscar el indice en diccionario (que letra es)
    // -> Ir sumando +1 al indice dependiendo de la clave, (3 => 1 + 1 + 1), para ver cuando llega al final
    // Si se pasa, volvemos a 0 y vuelve a empezar
    //-> Formamos la nueva frase añadiendo la letra cifrada al final de la frase
    for (var i = 0; i < this.entrada.length; i++) {
      var index = dictsplit.indexOf(this.entrada[i]);
      for (var j = 0; j < this.clau; j++) {
        if(index + 1 < 38){
          index++;
        } else {
          index = 0;
        }
      }
      nuevafrase = nuevafrase += dictsplit[index];
    }
    this.sortida = nuevafrase;
  }

  // para sacar sortida
  mostrarMissatge() {
    return this.sortida;
  }
}