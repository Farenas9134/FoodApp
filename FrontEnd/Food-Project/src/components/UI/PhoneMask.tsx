import { useId, type SVGProps } from "react";

type PhoneMaskProps = SVGProps<SVGSVGElement> & { src: string };

export const PhoneMask = ({ src, height = "100%", width = "100%", ...props }: PhoneMaskProps) => {
  const clipId = useId().replace(/:/g, "");

  return (
    <svg
      width={width}
      height={height}
      viewBox="-20 -20 453 930"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <defs>
        <clipPath id={clipId}>
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M116.674 32.8671H296.089C310.679 32.8671 322.506 21.095 322.506 5.20396C322.655 2.39518 324.912 0.148635 327.727 0.00708142L370.937 0C394.037 0 412.763 18.6391 412.763 41.6317V847.972C412.763 870.965 394.037 889.604 370.937 889.604H41.8267C18.7264 889.604 0 870.965 0 847.972V41.6317C0 18.6391 18.7264 0 41.8267 0H85.0293C87.8512 0.148635 90.1083 2.39518 90.2505 5.19688C90.2576 21.095 102.085 32.8671 116.674 32.8671Z"
          />
        </clipPath>
      </defs>

      <image
        href={src}
        x="0"
        y="0"
        width="413"
        height="890"
        preserveAspectRatio="xMidYMid slice"
        clipPath={`url(#${clipId})`}
      />
    </svg>
  );
};