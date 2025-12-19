import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'

type ComponentProps = {
  id: string
  name: string
  avatar_url: string
  username: string
}

const avatarButton: React.FC<ComponentProps> = ({ id, name, avatar_url, username }) => {
  return (
    <a onClick={}>
      <div className='flex flex-col items-center'>
        <Avatar className='h-16 w-16'>
          <AvatarImage src={avatar_url} />
          <AvatarFallback></AvatarFallback>
        </Avatar>
        <span className='text-xs text-center mt-2 text-zinc-600 w-16 h-5 truncate'>{name}</span>
      </div>
    </a>
  )
}

export default avatarButton
