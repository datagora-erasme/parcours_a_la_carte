import { FaCommentDots } from 'react-icons/fa';

const ButtonShareFeedback = () => {
  return (
    <div style={{ zIndex: 1000 }} className="fixed top-0 right-0 h-screen py-4 px-4 flex flex-col items-center">
      <button className="bg-primary rounded-full text-white py-4 px-5 flex items-center shadow-md">
        <FaCommentDots className="text-white mr-3" />
        <span className="underline underline-offset-2">
          Partager vos retours ici
        </span>
      </button>
    </div>
  )
}

export default ButtonShareFeedback;