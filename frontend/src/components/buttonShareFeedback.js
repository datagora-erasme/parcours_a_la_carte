import { useContext } from 'react';
import { FaCommentDots } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';

const ButtonShareFeedback = () => {
  const { isMobile } = useContext(MainContext);
  const openLink = () => {
    window.open("https://form.typeform.com/to/yP5LDsXk", "_blank")
  }

  return (
    <div style={{ zIndex: 1000 }} className="fixed top-0 right-0 h-screen p-4 flex flex-col items-center">
      <button onClick={openLink} className={`bg-primary rounded-full text-white flex items-center shadow-md ${isMobile ? 'p-3' : 'px-5 py-3'}`}>
        <FaCommentDots className="text-white" />
        {!isMobile && 
          <span className="underline underline-offset-2 ml-3">
            Partager vos retours ici
          </span>
        }
      </button>
    </div>
  )
}

export default ButtonShareFeedback;