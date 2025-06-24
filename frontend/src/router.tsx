import { RouteObject } from 'react-router-dom'
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
import TestPage from './pages/TestPage'
import TestResultPage from './pages/TestResultPage'

export const routes: RouteObject[] = [
  { path: '/', element: <MainMenu /> },
  { path: '/client', element: <ClientMenu /> },
  { path: '/server', element: <ServerMenu /> },
  { path: '/run', element: <TestSelector /> },
  { path: '/log', element: <LogPage /> },
  { path: '/stats', element: <StatisticsPage /> },
  { path: '/routine', element: <RoutinePage /> },
  { path: '/routine/add', element: <AddRoutine /> },
  { path: '/routine/saved', element: <GetRoutines /> },
  { path: '/results', element: <ResultsPage /> },
  { path: '/routine/:routineId/testes', element: <TestPage /> },
  { path: '/results/:testId/:routineId', element: <TestResultPage /> }
]
