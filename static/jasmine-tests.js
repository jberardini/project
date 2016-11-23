// describe("Hello world", function() {
//     it('says hello', function() {
//         expect(helloWorld()).toEqual('Hello world!');
//     });
// });

describe("My Test Suite", function () {

    it("should choose address search", function () {
        chooseAddressSearch();
        nabeVal = $('#neighborhood').val();
        expect(nabeVal).toBe('blank');

        

    });

    it("should choose neighborhood search", function () {
        chooseNeighborhoodSearch();
        addVal = $('#address').val();
        expect(addVal).toBe('');

        addresssearch = $('.address-search');
        expect(addresssearch).toBeHidden();

    });

});


// function chooseAddressSearch() {
//   $('#neighborhood').val('blank')
//   $('.neighborhood-search').hide();
//   $('.address-search').show();