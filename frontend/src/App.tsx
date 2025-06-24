import { Routes, Route } from 'react-router-dom'
import MainMenu from './pages/MainMenu'
import ClientMenu from './pages/ClientMenu'
import ServerMenu from './pages/ServerMenu'
import TestSelector from './pages/TestSelector'
import LogPage from './pages/LogPage'
import StatisticsPage from './pages/StatisticsPage'
import RoutinePage from './pages/RoutinePage'
import AddRoutine from './pages/AddRoutine'
import GetRoutines from './pages/GetRoutines'
import ResultsPage from './pages/ResultsPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<MainMenu />} />
      <Route path="/client" element={<ClientMenu />} />
      <Route path="/server" element={<ServerMenu />} />
      <Route path="/run" element={<TestSelector />} />
      <Route path="/log" element={<LogPage />} />
      <Route path="/stats" element={<StatisticsPage />} />
      <Route path="/routine" element={<RoutinePage />} />
      <Route path="/routine/add" element={<AddRoutine />} />
      <Route path="/routine/saved" element={<GetRoutines />} />
      <Route path="/results" element={<ResultsPage />} />
    </Routes>
  )
}