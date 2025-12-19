import { Button } from '@/components/ui/button'
import type { LucideIcon } from 'lucide-react'

type ButtonIconProps = {
  icon?: LucideIcon
}

export function MenuButton({ icon: Icon, ...props }: ButtonIconProps) {
  return (
    <Button variant='outline' size='icon' className='size-10 rounded-full' {...props}>
      {Icon && <Icon className='size-5' />}
    </Button>
  )
}
