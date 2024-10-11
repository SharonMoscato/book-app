function FancyButton({text, onClick}) {
  return (
    <button 
    onClick={onClick}
    className="bg-gradient-to-b w-max mx-auto text-blue-500 font-semibold from-slate-50 to-blue-100 px-10 py-3 rounded-2xl shadow-blue-400 shadow-md border-b-4 hover border-b border-blue-200 hover:shadow-sm transition-all duration-500">
      {text}
    </button>
  )
}

export default FancyButton