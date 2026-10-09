// @ts-ignore
import "../../css/PhoneFrame.css"
import { PhoneMask } from "./PhoneMask";

export function PhoneFrame({ picture }: { picture: string}) {
  return (
    <div className="relative w-[470px] h-[940px]">
      
      {/* 1. Main Phone Body */}
      <div className="w-full h-full bg-[#3A4245] rounded-[70px] relative shadow-2xl">
        {/* Inner Screen Container */}
        <div className="absolute inset-[8px] bg-black rounded-[58px] overflow-hidden">
          {/* Wallpaper / App Content Goes Here */}
          <PhoneMask src={picture}/>
        </div>
      </div>

      {/* Buttons below  */}

      {/* Speaker (Top-Middle) (left-1/2 grabs middle of frame) (-translate-x-1/2 does some weird stuff that moves speaker back left by 50% of own width)*/}
      <div className="absolute top-[27px] left-1/2 -translate-x-1/2 w-[56px] h-[7px] bg-[#262C2D] rounded-4xl"></div>
      {/* Camera, right of speaker */}
      <div className="absolute top-[22px] left-[272px] w-[18px] h-[18px]">
        <div className="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 w-4 h-4 rounded-full bg-[#262C2D]"></div>
        <div className="absolute top-1/2 -translate-y-1/2 left-1/2 -translate-x-1/2 w-[8px] h-[8px] rounded-full bg-black"></div>
        <div className="absolute top-[7px] left-1/2 -translate-x-1/2 w-[2px] h-[2px] rounded-full bg-[#262C2D]"></div>
      </div>
      {/* Third Button? (Top-Left) */}
      <div className="absolute top-[120px] -left-[3px] w-[3.3px] h-[26px] bg-[#121518] rounded-l-md" />

      {/* Volume Up (Left) */}
      <div className="absolute top-[165px] -left-[3px] w-[3.3px] h-[50px] bg-[#121518] rounded-l-md" />

      {/* Volume Down (Left) */}
      <div className="absolute top-[230px] -left-[3px] w-[3.3px] h-[50px] bg-[#121518] rounded-l-md" />

      {/* Power Button (Right Side) */}
      <div className="absolute top-[180px] -right-[3px] w-[3.3px] h-[75px] bg-[#121518] rounded-r-md" />

    </div>
  );
}

export default PhoneFrame