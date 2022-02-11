import useUnits from "../hooks/useUnits";
import "./search.css"

const Search = ({ handleChange, handleSubmit }) => {
    const units = useUnits();

    return (
        <section className="search transparentbox">
            <p>Enter a number you've encountered below (with a unit, if applicable)</p>
            <div>
                <input type="number" name="value" onChange={handleChange} placeholder="0"></input>
                {/* <button onClick={handleSubmit}>Search</button> */}
                <select name="unit" onChange={handleChange}>
                    {units.map(u => <option key={u.shortname} value={u.shortname}>{u.name}</option>)}
                </select>
            </div>
        </section>
    )
}

export default Search;