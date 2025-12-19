
import { CircleUser } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { MenuButton } from '../custom/menuButton'

export const Navbar = () => {
  const navigate = useNavigate()

  return (
    <div className='flex items-center px-2 h-12 w-full fixed z-10 bg-black/30 backdrop-blur-xl'>
      <a href='/' className='h-fit text-2xl'>
        💎 Miracle
      </a>
      <div className='flex items-center ml-auto gap-2'>
        <MenuButton icon={CircleUser} onClick={() => navigate('/profile')} />
      </div>
    </div>
  )
}
