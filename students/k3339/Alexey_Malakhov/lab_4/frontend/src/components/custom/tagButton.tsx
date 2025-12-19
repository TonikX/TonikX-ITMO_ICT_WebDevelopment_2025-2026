// components/overrides/RoundedButton.tsx
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import * as React from 'react'

type Props = React.ComponentProps<typeof Button>

export function TagButton({ className, size = 'default', ...rest }: Props) {
  return (
    <Button
      {...rest}
      size={size}
      className={cn(
        'rounded-full',
        size === 'default' && '[&>*:first-child]:ml-[-0.9rem]',
        size === 'lg' && '[&>*:first-child]:ml-[-1.4rem]',
        className
      )}
    />
  )
}
