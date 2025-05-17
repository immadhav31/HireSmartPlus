import React, { useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import { FiUploadCloud, FiCheckCircle } from 'react-icons/fi';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const UploadPage = () => {
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    document.title = "HireSmart+ | Resume Upload";
  }, []);

  const handleDrop = async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) return;

    setUploadedFiles(acceptedFiles);
    const formData = new FormData();
    formData.append("file", acceptedFiles[0]);

    try {
      const response = await fetch("https://hiresmartplus.onrender.com/resume/upload-resumes-zip/", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Upload response:", data);
        navigate('/formpage');
      } else {
        console.error("Upload failed:", response.statusText);
        alert('File upload failed. Only ZIP files allowed.');
      }
    } catch (error) {
      console.error("Upload failed:", error);
      alert('Network error. Please check your connection.');
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center p-6 overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
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
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 right-0 bottom-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-black/30 mix-blend-overlay"></div>
        
        <div className="absolute inset-0 opacity-30">
          <div className="absolute w-96 h-96 bg-blue-500/20 rounded-full blur-3xl animate-blob top-[-10%] left-[-10%]"></div>
          <div className="absolute w-80 h-80 bg-purple-500/20 rounded-full blur-3xl animate-blob animation-delay-2000 top-[50%] right-[-10%]"></div>
          <div className="absolute w-72 h-72 bg-pink-500/20 rounded-full blur-3xl animate-blob animation-delay-4000 bottom-[-10%] left-[50%]"></div>
        </div>

        <div className="absolute inset-0 bg-grid-white/5 pointer-events-none"></div>
      </div>

      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-xl bg-gray-800/60 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/10 p-10"
      >

        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-br from-white via-gray-200 to-blue-300 mb-4">
            Resume Upload
          </h1>
          <p className="text-gray-400 text-lg">
            Securely upload your professional documents
          </p>
        </div>

        <Dropzone onDrop={handleDrop}>
          {({ getRootProps, getInputProps, isDragActive }) => (
            <div
              {...getRootProps()}
              className={`
                relative z-10 border-2 rounded-xl p-10 text-center cursor-pointer transition-all duration-300
                ${isDragActive 
                  ? 'border-blue-500 bg-blue-900/30' 
                  : 'border-dashed border-gray-600 hover:border-blue-500'}
              `}
            >
              <input {...getInputProps()} className="absolute inset-0 z-20" />
              {uploadedFiles.length > 0 ? (
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="flex flex-col items-center"
                >
                  <FiCheckCircle className="text-6xl text-green-500 mb-4" />
                  <p className="text-gray-300">
                    {uploadedFiles.length} file{uploadedFiles.length > 1 ? 's' : ''} uploaded
                  </p>
                </motion.div>
              ) : (
                <>
                  <FiUploadCloud className="mx-auto text-6xl text-gray-500 mb-4" />
                  <p className="text-gray-400 text-lg">
                    {isDragActive 
                      ? 'Drop your files here' 
                      : 'Drag & drop your resume or click to upload'}
                  </p>
                </>
              )}
            </div>
          )}
        </Dropzone>

        <div className="text-center mt-6 text-gray-500 text-sm">
          Supported formats: zip
        </div>
      </motion.div>
    </div>
  );
};

export default UploadPage;
