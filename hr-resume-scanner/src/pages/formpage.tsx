import React, { useState, useEffect} from "react";
import { useNavigate } from "react-router-dom";

const ProcessingWithTheme = () => {
  const [formData, setFormData] = useState({
    skills: "",
    candidates: 5,
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processingDone, setProcessingDone] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    document.title = "HireSmart+ | Resume Upload";
    // Add timer to switch from processing to processed after 2 seconds
    const timer = setTimeout(() => {
      setProcessingDone(true);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    

    const payload = {
      skills: formData.skills.split(",").map((skill) => skill.trim()),
      candidates: formData.candidates,
    };

    try {
      const response = await fetch("http://localhost:8000/resume/api/hr/preferences/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      console.log("Top Candidates:", data.top_candidates);
      console.log("Total Applications:", data.total_applications);
      console.log("Matched Applications:", data.matched_applications);

      navigate("/finalpage", { 
        state: { 
          candidates: data.top_candidates,
          totalApplications: data.total_applications,
          matchedApplications: data.matched_applications,
          skillsKeyword: formData.skills
        } 
      });
    } catch (error) {
      console.error("Error submitting form:", error);
      setError("Failed to submit preferences. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-6 overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 right-0 bottom-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-black/30 mix-blend-overlay"></div>
        <div className="absolute inset-0 opacity-30">
          <div className="absolute w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-blob top-[-10%] left-[-10%]"></div>
          <div className="absolute w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-blob animation-delay-2000 top-[50%] right-[-10%]"></div>
          <div className="absolute w-72 h-72 bg-pink-500/20 rounded-full blur-3xl animate-blob animation-delay-4000 bottom-[-10%] left-[50%]"></div>
        </div>
        <div className="absolute inset-0 bg-grid-white/5 pointer-events-none"></div>
      </div>

      <div className="absolute top-6 left-1/2 transform -translate-x-1/2">
  <h1 className="text-4xl font-['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif']
                 font-bold 
                 text-white
                 tracking-tight
                 flex items-center
                 transition-all duration-300
                 hover:text-white-700
                 hover:scale-[1.02]">
    HireSmart
    <sup className="text-3.5xl font-extrabold text-white-400 ml--1.5 -top-1.5">+</sup>
  </h1>
</div>

      <div className="relative flex flex-row items-center justify-between w-full max-w-5xl bg-gradient-to-tr from-gray-800 to-gray-900 p-8 rounded-xl shadow-2xl mt-16 margin-top--10">
        <div className="w-1/2 flex justify-center items-center">
          <div className="relative">
            <div className="w-48 h-48 flex flex-col items-center justify-center">
              <div className="relative flex items-center justify-center">
                {processingDone ? (
                  <>
                    <div className="w-36 h-36 rounded-full border-8 border-t-8 border-blue-500 flex items-center justify-center bg-gradient-to-r from-white-400 to-green-600"></div>
                    <span className="absolute text-white text-6xl font-bold">✅</span>
                  </>
                ) : (
                  <>
                    <div className="w-36 h-36 rounded-full border-8 border-t-8 border-blue-500 border-t-purple-500 animate-spin"></div>
                    <span className="absolute text-white text-6xl font-bold">⏳</span>
                  </>
                )}
              </div>
            </div>
            <p className="text-center text-gray-300 mt-6">{processingDone ? "Processed" : "Processing..."}</p>
          </div>
        </div>

        <div className="w-1/2 bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold text-gray-100 mb-6">HR Preferences</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="skills" className="block text-gray-300 mb-2">
                Desired Skills (comma-separated)
              </label>
              <input
                type="text"
                id="skills"
                name="skills"
                placeholder="e.g., Python, Machine Learning"
                className="w-full px-4 py-2 border border-gray-600 rounded-lg shadow-sm bg-gray-900 text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                value={formData.skills}
                onChange={handleChange}
              />
            </div>

            <div className="mb-4">
              <label htmlFor="candidates" className="block text-gray-300 mb-2">
                Number of Candidates
              </label>
              <input
                type="number"
                id="candidates"
                name="candidates"
                placeholder="e.g., 5"
                className="w-full px-4 py-2 border border-gray-600 rounded-lg shadow-sm bg-gray-900 text-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-400"
                value={formData.candidates}
                onChange={handleChange}
              />
            </div>

            <button
              type="submit"
              className={`w-full text-white font-semibold py-2 rounded-lg transition ${
                isSubmitting ? "bg-gray-500 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
              }`}
              disabled={isSubmitting}
            >
              {isSubmitting ? "Submitting..." : "Submit Preferences"}
            </button>
            {error && <p className="text-red-500 mt-4">{error}</p>}
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProcessingWithTheme;