import React, { useEffect } from "react";
import { useLocation } from "react-router-dom";

interface Candidate {
    id: string;
    name: string;
    email: string;
    skills: string;
    similarity_score: number | null;
}

interface LocationState {
    candidates: Candidate[];
    totalApplications: number;
    matchedApplications: number;
    skillsKeyword: string;
}

const ResultsPage = () => {
    const location = useLocation();
    const { 
        candidates, 
        totalApplications, 
        matchedApplications, 
        skillsKeyword 
    } = location.state as LocationState;

    useEffect(() => {
        document.title = "HireSmart+ | Candidate Results";
    }, []);

    const convertToCSV = (data: Candidate[]) => {
        const headers = ["ID", "Name", "Email", "Skills"];
        const rows = data.map((candidate: Candidate) =>
            `${candidate.id},${candidate.name},${candidate.email},"${candidate.skills}"`
        );
        return [headers.join(","), ...rows].join("\n");
    };

    const downloadResultsAsCSV = () => {
        const csv = convertToCSV(candidates);
        const blob = new Blob([csv], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = "results.csv";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-8 flex flex-col items-center">
            <div className="absolute top-6 left-1/2 transform -translate-x-1/2">
                <h1 className="text-4xl font-bold text-white tracking-tight flex items-center transition-all duration-300 hover:text-white-700 hover:scale-[1.02]">
                    HireSmart
                    <sup className="text-4xl font-extrabold text-white-400 ml-1.0">+</sup>
                </h1>
            </div>

            <div className="w-full max-w-4xl bg-gray-800 p-6 rounded-lg shadow-lg mb-6 mt-16">
                <div className="grid grid-cols-3 gap-4 text-center">
                    <div className="p-4 border border-blue-500 rounded-lg bg-gray-700">
                        <h3 className="text-xl font-semibold">Total Applications</h3>
                        <p className="text-3xl text-blue-400">{totalApplications}</p>
                    </div>
                    <div className="p-4 border border-green-500 rounded-lg bg-gray-700">
                        <h3 className="text-xl font-semibold">Matched Applications</h3>
                        <p className="text-3xl text-green-400">{matchedApplications}</p>
                    </div>
                    <div className="p-4 border border-purple-500 rounded-lg bg-gray-700">
                        <h3 className="text-xl font-semibold">Skill Keyword</h3>
                        <p className="text-xl text-purple-400 break-all">{skillsKeyword || "N/A"}</p>
                    </div>
                </div>
            </div>

            <div className="flex items-center justify-center h-full"> 
                <div className="w-full max-w-4xl bg-gray-800 p-6 rounded-lg shadow-lg overflow-hidden">
                    <h2 className="text-2xl font-semibold mb-6 text-center">Top Matched Candidates</h2>
                    {candidates.length > 0 ? (
                        <table className="w-full border-collapse rounded-lg overflow-hidden">
                            <thead>
                                <tr className="bg-blue-600 text-left">
                                    <th className="p-4">Name</th>
                                    <th className="p-4">Email</th>
                                    <th className="p-4">Matched Skills</th>
                                    <th className="p-4">Score</th>
                                </tr>
                            </thead>
                            <tbody>
                                {candidates.map((candidate: Candidate, idx: number) => (
                                    <tr key={candidate.id || idx} className={idx % 2 === 0 ? "bg-gray-700" : "bg-gray-600"}>
                                        <td className="p-4">{candidate.name}</td>
                                        <td className="p-4">{candidate.email}</td>
                                        <td className="p-4 break-all">{candidate.skills}</td>
                                        <td className="p-4">
                                            {candidate.similarity_score !== null 
                                                ? candidate.similarity_score.toFixed(3) 
                                                : "N/A"}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <p className="text-lg font-medium text-center mt-4">No candidates found.</p>
                    )}
                    <button
                        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg shadow transition-transform transform hover:scale-[1.05]"
                        onClick={downloadResultsAsCSV}
                    >
                        Download Results
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultsPage;