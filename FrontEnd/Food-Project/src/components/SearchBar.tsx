import { FaSearch } from "react-icons/fa";

type SearchBarProps = { 
    value: string;
    onChange: (query: string) => void;
    onSearch: (query: string) => void;
    onFocus: () => void;
};

function SearchBar({ value, onChange, onSearch, onFocus }: SearchBarProps){
    return (
        <div className="flex justify-center font-display">
            <form onSubmit={(e) => {e.preventDefault(); onSearch(value)}} className="flex bg-[#FFFFFF] p-2 rounded-4xl border-1 border-[#CCC] text-[18px] w-full shadow gap-3 items-center">
                <FaSearch/>
                <input
                    type="text"
                    placeholder="Search recipes by name, id, or tags..."
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="flex justify-center border-none outline-none w-full"
                    onFocus={onFocus}
                />
            </form>
        </div>
    )
}

export default SearchBar