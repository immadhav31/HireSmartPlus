import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import UploadPage from "./pages/uploadpage";
import FormPage from './pages/formpage';
import FinalPage from './pages/finalpage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/formpage" element={<FormPage />} />
        <Route path="/finalpage" element={<FinalPage />} />
      </Routes>
    </Router>
  );
};

export default App;