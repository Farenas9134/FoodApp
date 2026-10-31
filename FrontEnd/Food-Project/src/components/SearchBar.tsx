type SearchBarProps = { 
    value: string;
    onChange: (query: string) => void;
    onSearch: (query: string) => void
};

function SearchBar({ value, onChange, onSearch }: SearchBarProps){
    return (
        <div className="flex justify-center font-display">
            <form onSubmit={(e) => {e.preventDefault(); onSearch(value)}} className="bg-[#FFFFFF] p-2 rounded-4xl border-1 border-[#CCC] text-[18px] w-[35%]">
                <input
                    type="text"
                    placeholder="Search recipes by name, id, or tags..."
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    className="flex justify-center border-none outline-none w-full"
                />
            </form>
        </div>
    )
}

export default SearchBar