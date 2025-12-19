import { Navbar } from './components/layout/Navbar'
import SignUp from '@/pages/SignUp'
import LogIn from '@/pages/LogIn'
import Main from '@/pages/Main'
import Profile from '@/pages/Profile'
import { Route, Routes } from 'react-router-dom'

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path='/' element={<Main />}></Route>
        <Route path='/signup' element={<SignUp />}></Route>
        <Route path='/login' element={<LogIn />}></Route>
        <Route path='/profile' element={<Profile />}></Route>
      </Routes>
    </>
  )
}

export default App
