
function imprimerSections1() {
    // Style pour garantir exactement 3 pages
    const style = `
        <style>
            @page {
                size: A4; /* Taille standard */
                margin: 0; /* Supprime les marges ajoutées par l'imprimante */
            }
            @media print {
                body {
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }
                .proforma, .facture_definitive, .bon_livraison {
                    width: 100%;
                    height: 100vh; /* Chaque section occupe exactement une page */
                    page-break-before: always; /* Forcer chaque section à commencer sur une nouvelle page */
                    page-break-after: avoid; /* Empêcher une section d’être coupée */
                    padding-top: 100px;
                }
                .proforma:first-of-type {
                    page-break-before: auto; /* Pas de saut avant la première section */
                }
                .btn, .card-header {
                    display: none; /* Cache les boutons */
                }
            }
        </style>
    `;

    // Récupérer tout le contenu à imprimer
    const contenu = document.getElementById("proforma1").outerHTML + document.getElementById("facture_definitive1").outerHTML + document.getElementById("bon_livraison1").outerHTML;

    // Créer une nouvelle page avec le style et le contenu
    
    for(i=0; i<3; i++){
        const pageImpression = document.createElement("div");
        pageImpression.innerHTML = style + contenu;

        // Ajouter temporairement au body
        document.body.appendChild(pageImpression);

        // Imprimer
        window.print();

        // Nettoyer après impression
        document.body.removeChild(pageImpression);
        i++
    }
    
}





const separateur = document.querySelectorAll('.separateur')
separateur.forEach((element)=>{
    const value = element.textContent.trim(); 
    if (!isNaN(value) && value !== "") { 
        const formattedNumber = Number(value).toLocaleString('fr-FR'); 
        element.textContent = formattedNumber; 
    }
})

function numberToWordsFR(n) {
  if (n < 0) return "moins " + numberToWordsFR(-n);
  if (n === 0) return "zéro";

  const units = [
      "", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"
  ];
  const teens = [
      "dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", 
      "dix-sept", "dix-huit", "dix-neuf"
  ];
  const tens = [
      "", "", "vingt", "trente", "quarante", "cinquante", 
      "soixante", "soixante", "quatre-vingt", "quatre-vingt"
  ];

  const scales = ["", "mille", "million", "milliard"];

  function convert_hundreds(num) {
      let result = "";

      if (num >= 100) {
          const hundreds = Math.floor(num / 100);
          if (hundreds > 1) result += units[hundreds] + " cent";
          else result += "cent";
          if (num % 100 === 0) return result;
          result += num % 100 > 0 ? " " : "";
          num %= 100;
      }

      if (num >= 20) {
          const ten = Math.floor(num / 10);
          result += tens[ten];
          if (ten === 7 || ten === 9) {
              result += "-" + teens[num % 10];
          } else if (num % 10 > 0) {
              result += (ten === 8 ? "-" : "-") + units[num % 10];
          }
      } else if (num >= 10) {
          result += teens[num - 10];
      } else if (num > 0) {
          result += units[num];
      }

      return result;
  }

  function convert_thousands(num) {
      let result = "";
      let scaleIndex = 0;

      while (num > 0) {
          const chunk = num % 1000;

          if (chunk > 0) {
              const chunkText = convert_hundreds(chunk);
              if (scaleIndex > 0) {
                  result = chunkText + " " + scales[scaleIndex] + (chunk > 1 && scaleIndex > 1 ? "s" : "") + " " + result;
              } else {
                  result = chunkText + " " + result;
              }
          }

          num = Math.floor(num / 1000);
          scaleIndex++;
      }
      return result.trim();
  }
  return convert_thousands(n);
}

const nombrelettre = document.querySelector('.lettre')
const nombrelettres = document.querySelector('.lettres')
nombrelettre.innerHTML = numberToWordsFR(parseInt(nombrelettre.innerText, 10)) + ' DE FRANCS CFA./.'
nombrelettres.innerHTML = numberToWordsFR(parseInt(nombrelettres.innerText, 10))  + ' DE FRANCS CFA./.'
