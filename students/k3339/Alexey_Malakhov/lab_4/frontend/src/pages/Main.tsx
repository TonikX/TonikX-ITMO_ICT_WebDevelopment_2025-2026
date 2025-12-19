import { Separator } from '@/components/custom/separator'
import Authors from '@/components/layout/Authors'
import Posts from '@/components/layout/Posts'
import { useState } from 'react'
import PostCreation from '@/components/layout/PostCreation'

const Main = () => {
  const [activeAuthor, setActiveAuthor] = useState<number | null>(null)

  return (
    <>
      <Authors activeAuthor={activeAuthor} onSelectAuthor={setActiveAuthor} />
      <Separator />
      {/* <Separator /> */}
      {/*<Photos />*/}
      {/* <Separator /> */}
      <div className='flex justify-center'>
        <PostCreation />
      </div>
      <div className='flex justify-center'>
        <Posts activeAuthor={activeAuthor} />
      </div>
    </>
  )
}

export default Main
