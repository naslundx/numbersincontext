import useUnits from "../hooks/useUnits";

const Search = ({ handleChange, handleSubmit }) => {
    const units = useUnits();

    return (
        <div className="search">
            <input type="number" name="value" onChange={handleChange}></input>
            {/* <button onClick={handleSubmit}>Search</button> */}
            <select name="unit" onChange={handleChange}>
                {units.map(u => <option key={u.id} value={u.id}>{u.name}</option>)}
            </select>
        </div>
    )
}

export default Search;