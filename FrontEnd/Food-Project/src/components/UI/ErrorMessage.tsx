import React from "react";
import { BiErrorCircle, BiRefresh, BiHomeAlt } from "react-icons/bi";
import { Link } from "react-router-dom";

interface ErrorMessageProps {
  err: string;
}

function ErrorMessage({ err }: ErrorMessageProps): React.ReactElement {
  return (
    <div className="flex flex-col items-center justify-center w-full max-w-lg mx-auto my-8 p-8 bg-[#FFFDF7] border border-[#EBE5D8] rounded-2xl shadow-lg text-center font-display">
        {/* Error Icon */}
        <div className="flex items-center justify-center w-14 h-14 bg-[#FDF2F0] rounded-full mb-4 text-[#C1622D]">
            <BiErrorCircle className="w-8 h-8" />
        </div>

        {/* Generic message (maybe change?) */}
        <h3 className="text-2xl font-bold text-[#183C04] mb-2">
            Something went wrong
        </h3>

        {/* Main error message or alt if none found */}
        <p className=" text-[#183C04]/80 mb-4">
            {err || "We encountered an error while loading your recipe data. Don't worry, your saved items and pantry are safe. If problem continues, please don't be afraid to conatact us for help!"}
        </p> 

        <div className="flex flex-wrap items-center justify-center gap-3 w-full">
            <Link
                to="/"
                className="flex items-center justify-center gap-2 px-5 py-2.5 bg-[#183C04] hover:bg-[#122e03] text-white font-medium text-sm rounded-full transition-all duration-200 shadow-sm">
                <BiHomeAlt className="w-4 h-4" />
                Back to Home
            </Link>
        </div>
    </div>
  );
}

export default ErrorMessage;