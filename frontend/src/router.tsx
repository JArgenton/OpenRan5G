import { createBrowserRouter } from "react-router-dom";
import MainMenu from "./pages/MainMenu";
import TestSelector from "./pages/TestSelector";
import ClientMenu from "./pages/ClientMenu";
import ServerMenu from "./pages/ServerMenu";
import LogPage from "./pages/LogPage";
import StatisticsPage from "./pages/StatisticsPage";
import RoutinePage from "./pages/RoutinePage";
import AddRoutine from "./pages/AddRoutine";
import ResultsPage from "./pages/ResultsPage";
import GetRoutines from "./pages/GetRoutines";



const router = createBrowserRouter([
    {
        path: "/",
        element: <MainMenu />
    },{
        path: "/client",
        element: <ClientMenu />
    },{
        path: "/server",
        element: <ServerMenu />
    },{
        path: "/run",
        element: <TestSelector />
    },{
        path: "/log",
        element: <LogPage />
    },{
        path: "/stats",
        element: <StatisticsPage />
    },{
        path: "/routine",
        element: <RoutinePage />
    },{
        path: "/routine/add",
        element: <AddRoutine />
    },{
        path: "/routine/saved",
        element: <GetRoutines />
    },{
        path: "/results",
        element: <ResultsPage />
    }
])

export default router