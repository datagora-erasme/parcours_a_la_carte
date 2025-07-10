import { FaExternalLinkAlt } from "react-icons/fa";

const ReadMore = () => {
  const openLink = () => {
    window.open("https://datagora.erasme.org/projets/parcours-a-la-carte/", "_blank")
  }
  return (
    <div className="w-full text-start">
      <div className="font-bold pt-1 mb-2">En savoir plus</div>
      <div className="my-4">
        <span className="bg-primary text-white rounded-full px-3 py-1 text-sm">Clic gauche :</span> Déplacer la caméra
      </div>
      <div className="mb-4">
        <span className="bg-primary text-white rounded-full px-3 py-1 text-sm">Molette haut-bas :</span> Zoom avant et arrière
      </div>
      <div>
        Parcours à la carte est une plateforme qui transforme vos déplacements dans la Métropole de Lyon. Grâce à cette application, explorez la ville à pied en privilégiant le confort et la découverte, avec des itinéraires personnalisés selon vos préférences : fraîcheur, calme, faible exposition au pollen ou encore points touristiques.
        <br></br><br></br>
        Cette expérimentation est menée par le service ERASME de la Métropole de Lyon.
      </div>
      <div className="flex justify-around items-center gap-8 w-full py-4">
        <img src="/logo_metropole.png" alt="Métropole Grand Lyon" className="h-14" />
        <img src="/logo_datagora.png" alt="DatAgora" className="h-16" />
      </div>
      <div className="flex items-center">
        <span className="underline underline-offset-2">
          Consulter le projet sur le site DatAgora
        </span>
        <span>
          <FaExternalLinkAlt className="text-primary ml-1 cursor-pointer" onClick={openLink} />
        </span>
      </div>
    </div>
  )
}

export default ReadMore;